

import re;



bnu_list = [850472078, 1056925222, 195148269, 777013031, 638385816, 711242461, 554567155]


def is_bnugroup(groupid):
    global bnu_list
    if groupid in bnu_list:
        return True
    else:
        return False



def is_bnu_studentid(id_str):
    pattern = "20[1-2][0-9][1-3][1-6][0-9][0-9][0-9][0-9][0-9][0-9]"
    searchobj = re.search(pattern, id_str);
    if searchobj:
        return True;
    else:
        return False;


