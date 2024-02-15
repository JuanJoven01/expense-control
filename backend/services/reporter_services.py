from db.db import Session

from db.models.models import Incomes, Categories, Expenses

from sqlalchemy import select

from services.sql_services import to_dict
from services.teams_services import __verify_if_user_in_teams__

import locale

from bokeh.embed import file_html
from bokeh.resources import CDN

##### Pie chart
from math import pi

from bokeh.io import show
from bokeh.models import (AnnularWedge, ColumnDataSource,
                          Legend, LegendItem, Plot, Range1d)
### end pie chart

def get_incomes_per_category(user_id: int):
    try:
        with Session() as session:
            query = (
                select(Incomes, Categories)
                .join(Categories, Categories.id == Incomes.category_id)
                .where(Categories.user_id == user_id)
            )
            incomes_per_category = session.execute(query).fetchall()
            incomes_per_category_dict = [{to_dict(income[1])['name']: to_dict(income[0])} for income in incomes_per_category]
            incomes_list = {}
            for dictionary in incomes_per_category_dict:
                for key, value in dictionary.items():
                    if key in incomes_list:
                        incomes_list[key].append(value)
                    else:
                        incomes_list[key] = [value]
            return incomes_list
    except Exception as e:
        return {'service error': str(e)}


def get_expenses_per_category(user_id: int):
    try:
        with Session() as session:
            query = (
                select(Expenses, Categories)
                .join(Categories, Categories.id == Expenses.category_id)
                .where(Categories.user_id == user_id)
            )
            expenses_per_category = session.execute(query).fetchall()
            expenses_per_category_dict = [{to_dict(income[1])['name']: to_dict(income[0])} for income in expenses_per_category]
            expenses_list = {}
            for dictionary in expenses_per_category_dict:
                for key, value in dictionary.items():
                    if key in expenses_list:
                        expenses_list[key].append(value)
                    else:
                        expenses_list[key] = [value]
            return expenses_list
    except Exception as e:
        return {'service error': str(e)}
    

def get_team_incomes_per_category(username:str, team_id: int):
    try:    
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                query = (
                    select(Incomes, Categories)
                    .join(Categories, Categories.id == Incomes.category_id)
                    .where(Categories.team_id == team_id)
                )
                incomes_per_category = session.execute(query).fetchall()
                print('+++'*30)
                print(incomes_per_category)
                incomes_per_category_dict = [{to_dict(income[1])['name']: to_dict(income[0])} for income in incomes_per_category]
                incomes_list = {}
                for dictionary in incomes_per_category_dict:
                    for key, value in dictionary.items():
                        if key in incomes_list:
                            incomes_list[key].append(value)
                        else:
                            incomes_list[key] = [value]
                return incomes_list
        return {'error message': 'looks like user is not in this team'}
    except Exception as e:
        return {'service error': str(e)}
    

def get_team_expenses_per_category(username:str, team_id: int):
    try:
        if __verify_if_user_in_teams__(username, team_id):
            with Session() as session:
                query = (
                    select(Expenses, Categories)
                    .join(Categories, Categories.id == Expenses.category_id)
                    .where(Categories.team_id == team_id)
                )
                expenses_per_category = session.execute(query).fetchall()
                expenses_per_category_dict = [{to_dict(income[1])['name']: to_dict(income[0])} for income in expenses_per_category]
                expenses_list = {}
                for dictionary in expenses_per_category_dict:
                    for key, value in dictionary.items():
                        if key in expenses_list:
                            expenses_list[key].append(value)
                        else:
                            expenses_list[key] = [value]
                return expenses_list
        return {'error message': 'looks like user is not in this team'}
    except Exception as e:
        return {'service error': str(e)}
    

def get_just_values_per_cat(data: object):
    try:
        total_per_category = {}
        for keys, values in data.items():
            total_per_category[keys] = 0
            for value in values:
                total_per_category[keys] += value["amount"]
        return total_per_category

    except Exception as e:
        return {'service error': str(e)}
    

def draw_donut_chart(data: object):
    try:
        xdr = Range1d(start=-2, end=2)
        ydr = Range1d(start=-2, end=2)

        plot = Plot(x_range=xdr, y_range=ydr)
        # plot.title.text = "Incomes reporter"
        # plot.toolbar_location = None

        total = sum(data.values())
        angles = [2 * pi * (value / total) for value in data.values()]
        for i in range(len(angles)):
            if i > 0:
                angles[i] = angles[i] + angles[i-1]

        colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown'] 
        source = ColumnDataSource(dict(
            start=[0] + angles[:-1],
            end=angles,
            colors=colors[:len(data)],
        ))

        glyph = AnnularWedge(x=0, y=0, inner_radius=0.9, outer_radius=1.8,
                            start_angle="start", end_angle="end",
                            line_color="white", line_width=3, fill_color="colors")
        
        r = plot.add_glyph(source, glyph)

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        legend = Legend(items=[
            LegendItem(label=f'{key}: {locale.currency(value, grouping=True)}', renderers=[r], index= i ) for i, (key, value) in enumerate(data.items())
        ], location="center")
        
        plot.add_layout(legend, "center")

        show(plot)

        html = file_html(plot, CDN, "my plot")
        return html
    except Exception as e:
        return {'service error': str(e)}

