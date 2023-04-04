import pandas as pd

def get_csv(csv):

    df = pd.read_csv(csv)
    row_3_values = df.iloc[2, :].values.tolist()

    pizza_data = pd.read_csv('pizzeria.csv')
    for index, row in pizza_data.iterrows():
        variable_name = f'variable{index + 1}'
        variable_data = f'Name: {row["Name"]} \nPrice: {row["Price"]} $ \nSize: {row["Size"]} \nToppings: "{row["Toppings"]}"'
        template_variables = {variable_name: variable_data}
        print(variable_name)
        #return render_template('shop.html', **template_variables)

    #for value in row_3_values:
        #print(value)
    #
    # for index, row in df.iterrows():
    #     print("Name : " + row['Name'])
    #     print("Price : " + str(row['Price']) + "$")
    #     print("Size : " + row['Size'])
    #     print("Toppings : " + row['Toppings'])
    #     print()
x1 = get_csv("pizzeria.csv")