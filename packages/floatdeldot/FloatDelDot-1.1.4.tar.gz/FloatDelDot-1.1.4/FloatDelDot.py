def default(res):
    res_list = list(str(res))

    try:
        index_list = res_list.index(".")

    except:
        try:
            return int(res)

        except:
            return print("Error! Instead of 'int' or 'float', you typed 'str' and it contains characters or some dots!")

    change_len = 2 #this num indicates how many digits will be after the dot

    try:
        for i in range(1, change_len + 1):
            try:
                if res == 0.0:
                    res = 0
                    return res

                if res_list[0] != "0":
                    if res_list[index_list + i] == "0":
                        if i == change_len:
                            return round(float(res))

                    else:
                        return round(float(res), change_len)

                else:
                    return round(float(res), (change_len + 6))

            except:
                return round(float(res))

    except:
        return print("Error! Instead of 'int' or 'float', you typed 'str' and it contains characters or some dots!")




def custom(res, change_len):
    res_list = list(str(res))

    try:
        index_list = res_list.index(".")

    except:
        try:
            return int(res)

        except:
            return print("Error! Instead of 'int' or 'float', you typed 'str' and it contains characters or some dots!")

    try:
        for i in range(0, change_len + 1):
            try:
                if res == 0.0:
                    res = 0
                    return res

                if res_list[0] != "0":
                    if res_list[index_list + i] == "0":
                        if i == change_len:
                            print("xx")
                            return round(float(res))

                    else:
                        if change_len == 0:
                            return round(float(res))
                        else:
                            return round(float(res), change_len)

                else:
                    return round(float(res), (change_len + 6))

            except:
                return round(float(res))

    except:
        return print("Error! Instead of 'int' or 'float', you typed 'str' and it contains characters or some dots!")