"""""""""""""""""""""""""""""
Project: wxtools
Author: Terance Jiang
Date: 1/16/2024
"""""""""""""""""""""""""""""
import multiprocessing

from tqdm import tqdm
from typing import Callable

from wxtools.logger.logger import setup_logger

logger = setup_logger(__name__, log_file=None, log_level='INFO')


def run_mlpro(worker: Callable, data: list, num_process: int = 10) -> list:
    """
    run worker with multiprocessing
    :param worker:  worker function
    :param data:  list of data
    :param num_process:  number of processes
    :return:  list of results or empty list
    """
    pool = multiprocessing.Pool(num_process)
    output = []
    for _ in tqdm(pool.imap_unordered(worker, data), total=len(data)):
        if _ is not None:
            output.append(_)

    pool.close()
    pool.join()

    return output
