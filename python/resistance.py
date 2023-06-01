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
    basic_value = data[0] + data[1]
    basic_value = float(basic_value)
    basic_value = round(basic_value)
    multiplier = basic_value * data[2]
    try :
        tolerance = round(data[3])
    except TypeError :
        tolerance = "null"
    result = [multiplier, tolerance]
    return result


def find_color_values(color_list, color_values) :
    result=[]
    for i in range(len(color_list)) :
        for row in color_values :
            if row["color"] == color_list[i] :
                if i == 0 :
                    result.append(row["first"])
                elif i == 1 :
                    result.append(row["second"])
                elif i == 2 :
                    result.append(float(row["multiplier"]))
                else :
                    try :
                        result.append(float(row["tolerance"]))
                    except ValueError :
                        result.append(row["tolerance"])
    return result


print(random_resistance())