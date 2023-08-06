#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : aizoo.
# @File         : data_utils
# @Time         : 2022/4/12 下午6:20
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


import torch
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split as _train_test_split

# ME
from meutils.pipe import *


class Data(object):

    def __init__(self, batch_size=128, cache_filename=""):
        self.batch_size = batch_size
        self.cache_filename = cache_filename

    def train_test_split(self, *arrays, test_size=0.2, random_state=42, stratify=None):
        f"""{_train_test_split.__doc__}"""

        # todo支持时间序列数据
        _ = _train_test_split(*arrays,
                              test_size=test_size,
                              random_state=random_state,
                              stratify=stratify)

        return self.from_cache(*_[::2]), self.from_cache(*_[1::2], is_train=False)

    def from_cache(self, *inputs, is_train=True):
        """
        出入参长度一致
        """
        # 输入
        logger.info(f"The {'train' if is_train else ' test'}'s shape: {inputs[0].shape}")

        # combine featues and labels of dataset

        dataset = TensorDataset(*self.array2tensor(inputs))

        # put dataset into DataLoader
        dataloader = DataLoader(
            dataset=dataset,  # torch TensorDataset format
            batch_size=self.batch_size,  # mini batch size
            shuffle=is_train,  # whether shuffle the data or not
            num_workers=0,  # read data in multithreading
        )

        return dataloader

    def save(self, ds, filename):
        """torch.save / joblib.dump"""
        return torch.save(ds, filename)

    def load(self, filename):
        return torch.load(filename)

    @staticmethod
    def array2tensor(arrays) -> List[torch.Tensor]:
        data = []
        for a in arrays:
            assert isinstance(a, (list, pd.Series, np.ndarray, pd.DataFrame, torch.Tensor)), "`arrays` Data Type Error"

            if isinstance(a, torch.Tensor):
                pass

            elif isinstance(a, (list, pd.Series, np.ndarray)):
                a = torch.Tensor(a)

            elif isinstance(a, pd.DataFrame):
                a = a.values.tolist()

            data.append(a)

        return data


if __name__ == '__main__':
    X = np.random.random((1000, 2))
    y = X @ (2, 1) + 1
    ds = Data(batch_size=5).from_cache(X, y)

    # print(ds | xnext)
