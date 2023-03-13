from models import Menu
from schemas.menu import VOMenuTree


def filter_menu_to_tree(data: list[Menu], parent_id: int = 0) -> list[VOMenuTree]:
    tree_data: list[VOMenuTree] = []
    for item in data:
        if item.parent_id == parent_id:
            temp: VOMenuTree | Menu = item
            temp.children = filter_menu_to_tree(data=data, parent_id=item.menu_id)
            tree_data.append(temp)
    return tree_data
