"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import torch


class GradCam:
    def __init__(self, model, layer_name):
        self.model = model
        self.layer_name = layer_name
        self.gradient = None
        self.activation = None
        self.hook_layers()

    def hook_layers(self):
        def get_activation(module, input, output):
            self.activation = output.detach()

        def get_gradient(grad):
            self.gradient = grad

        layer = dict([*self.model.named_modules()])[self.layer_name]
        layer.register_forward_hook(get_activation)
        layer.register_backward_hook(lambda module, grad_in, grad_out: get_gradient(grad_out[0]))

    def generate_heatmap(self, input_tensor, class_idx):
        # Forward pass
        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = torch.argmax(output)

        # Zero gradients
        self.model.zero_grad()

        # Backward pass with the selected class
        class_loss = output[0][class_idx]
        class_loss.backward()

        # Generate heatmap
        pooled_gradients = torch.mean(self.gradient, dim=[0, 2, 3])
        for i in range(self.activation.size(1)):
            self.activation[:, i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(self.activation, dim=1).squeeze()
        heatmap = torch.clamp(heatmap, min=0)

        # Normalize the heatmap
        heatmap /= torch.max(heatmap)

        return heatmap