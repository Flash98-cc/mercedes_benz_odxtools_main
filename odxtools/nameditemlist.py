# SPDX-License-Identifier: MIT
# Copyright (c) 2022 MBition GmbH

from typing import Callable, Dict, Iterable, List, Optional, Union, Generic, TypeVar

T = TypeVar('T')


class NamedItemList(Generic[T]):
    """A list that provides direct access to its items as named attributes.

    This is a hybrid between a list and a user-defined object: One can
    iterate over all items of the list as usual, but items can also be
    accessed via `named_list.itemname`, where the 'itemname' is
    specified via a item -> string mapping function that is passed to
    the constructor.

    If an item name is not unique, `_<num>` will be appended to
    avoid naming collisions. The user is responsible that the strings
    returned by the item-to-name function are valid identifiers in python.
    """

    # Callable[[T],str]表示参数类型是T，返回值类型是str，在这里作用是类型检查，检查传入的参数是否是可调用的参数
    # Iterable[T]一次返回一个类型为T的对象
    # self._item_to_name_fn = item_to_name_fn 相当于一个函数，输入一个类型T，输出一个str，
    # 以NamedItemList(lambda x: x.short_name, tmp)为例，输入一个tmp（diaglayercontainer类型）
    # 输出这个对象的short_name属性
    def __init__(self, item_to_name_fn: Callable[[T], str], input_list: Iterable[T] = None):

        self._item_to_name_fn = item_to_name_fn
        self._list: List[T] = []
        # TODO (?): This duplicates self.__dict__ -> Is there a prettier type-safe way?
        self._typed_dict: Dict[str, T] = {}

        if input_list is not None:
            for item in input_list:
                self.append(item)

    def append(self, item: T):
        """
        Append a new item to the list and make it accessible as a
        member attribute.

        \return The name under which item is accessible
        """
        self._list.append(item)

        item_name = self._item_to_name_fn(item)  # 返回一个str
        i = 1
        tmp = item_name
        while True:
            if tmp not in self.__dict__:
                self.__dict__[tmp] = item
                self._typed_dict[tmp] = item
                # print(tmp)
                return tmp

            i += 1
            tmp = f"{item_name}_{i}"

    def sort(self, key=None, reverse=False):
        return self._list.sort(key=key, reverse=reverse)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, key: Union[int, str]) -> Optional[T]:
        if isinstance(key, int):
            return self._list[key]
        else:
            return self._typed_dict.get(key)

    def __eq__(self, other: object) -> bool:
        """
        Named item lists are equal if the underlying lists are equal.
        Note that this does not consider the map `item_to_name_fn`.
        """
        if not isinstance(other, NamedItemList):
            return False
        else:
            return self._list == other._list

    def __iter__(self):
        return iter(self._list)

    def __str__(self):
        return f"[{', '.join([self._item_to_name_fn(s) for s in self._list])}]"

    def __repr__(self):
        return self.__str__()
