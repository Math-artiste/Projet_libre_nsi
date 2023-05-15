def random_resistance() :
    import csv
    from random import randint
    color=[]
    stack_data=[]
    with open("csv_files\color_resistance.csv", "r") as f :
        dataset = csv.DictReader(f, delimiter=',')
        for color_value in dataset :
            stack_data.append(color_value)
            color.append(color_value["color"])
    while len(color) != 4 :
        random_color_to_delete = randint(0,len(color)-1)
        del color[random_color_to_delete]
    parse_data = find_color_values(color, stack_data)
    resistance_value= calculate_R_value(parse_data)
    return color, resistance_value


def calculate_R_value(data) :
    basic_value = round(data[0] + data[1])
    multiplier = round(basic_value * data[2])
    tolerance = data[3]
    result = [multiplier, tolerance]
    return result


def find_color_values(color_list, color_values) :
    result=[]
    for i in range(len(color_list)) :
        for row in color_values :
            if row["color"] == color_list[i] :
                try :
                    if i == 0 :
                        result.append(float(row["first"]))
                    elif i == 1 :
                        result.append(float(row["second"]))
                    elif i == 2 :
                        result.append(float(row["multiplier"]))
                    else :
                        result.append(float(row["tolerance"]))
                except TypeError :
                    result.append(" ")
    return result


print(random_resistance())