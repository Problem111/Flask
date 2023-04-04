# script.py

import pandas as pd

# read data from a CSV file
df = pd.read_csv('pizzeria.csv')

# create HTML code for each row in the dataframe
rows_html = ''
for _, row in df.iterrows():
    row_html = f'''
    <div class="col mb-5">
        <div class="card h-100">
            <img class="card-img-top" src="{row['image_url']}" alt="..." />
            <div class="card-body p-4">
                <div class="text-center">
                    <h5 class="fw-bolder">{row['product_name']}</h5>
                    <p>{row['product_price']}</p>
                </div>
            </div>
        </div>
    </div>
    '''
    rows_html += row_html

# create the final HTML code with the rows
cards_html = f'''
<section class="py-5">
    <div class="container px-4 px-lg-5 mt-5">
        <div class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center">
            {rows_html}
        </div>
    </div>
</section>
'''

# write the HTML code to a file
with open('shop.html', 'w') as f:
    f.write(cards_html)