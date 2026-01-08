import matplotlib

matplotlib.use('Agg')

import logging
from django.shortcuts import render
from .models import Ditina
import plotly.graph_objs as go
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

base_data_male = [
    (0.0, 44.2, 46.1, 48.0, 49.9, 51.8, 53.7, 55.6),
    (0.25, 48.9, 50.8, 52.8, 54.7, 56.7, 58.6, 60.6),
    (0.5, 52.4, 54.4, 56.4, 58.4, 60.4, 62.4, 64.4),
    (1.0, 68.6, 71.0, 73.4, 75.7, 78.1, 80.5, 82.9),
    (2.0, 78.0, 81.0, 84.1, 87.1, 90.2, 93.2, 96.3),
    (3.0, 85.0, 88.7, 92.4, 96.1, 99.8, 103.5, 107.2),
    (4.0, 90.7, 94.9, 99.1, 103.3, 107.5, 111.7, 115.9),
    (5.0, 96.1, 100.7, 105.3, 110.0, 114.6, 119.2, 123.9),
    (6.0, 101.5, 106.5, 111.5, 116.5, 121.5, 126.5, 131.5),
    (7.0, 106.5, 111.7, 116.9, 122.1, 127.3, 132.5, 137.7),
    (8.0, 111.2, 116.8, 122.4, 128.0, 133.6, 139.2, 144.8),
    (9.0, 115.7, 121.7, 127.7, 133.7, 139.7, 145.7, 151.7),
    (10.0, 120.3, 126.7, 133.1, 139.5, 145.9, 152.3, 158.7),
    (11.0, 125.0, 132.0, 139.0, 146.0, 153.0, 160.0, 167.0),
    (12.0, 130.5, 137.9, 145.3, 152.7, 160.1, 167.5, 174.9),
    (13.0, 136.5, 144.9, 153.3, 161.7, 170.1, 178.5, 186.9),
    (14.0, 142.1, 151.0, 159.9, 168.8, 177.7, 186.6, 195.5),
    (15.0, 147.0, 155.5, 164.0, 172.5, 181.0, 189.5, 198.0),
    (16.0, 150.0, 158.0, 166.0, 174.0, 182.0, 190.0, 198.0),
    (17.0, 151.5, 159.5, 167.5, 175.5, 183.5, 191.5, 199.5),
    (18.0, 152.0, 160.0, 168.0, 176.0, 184.0, 192.0, 200.0),
]

base_data_female = [
    (0.0, 44.2, 46.1, 48.0, 49.9, 51.8, 53.7, 55.6),
    (0.25, 48.9, 50.8, 52.8, 54.7, 56.7, 58.6, 60.6),
    (0.5, 52.4, 54.4, 56.4, 58.4, 60.4, 62.4, 64.4),
    (1.0, 68.6, 71.0, 73.4, 75.7, 78.1, 80.5, 82.9),
    (2.0, 78.0, 81.0, 84.1, 87.1, 90.2, 93.2, 96.3),
    (3.0, 85.0, 88.7, 92.4, 96.1, 99.8, 103.5, 107.2),
    (4.0, 90.7, 94.9, 99.1, 103.3, 107.5, 111.7, 115.9),
    (5.0, 96.1, 100.7, 105.3, 110.0, 114.6, 119.2, 123.9),
    (6.0, 100.7, 105.4, 110.1, 114.8, 119.5, 124.2, 128.9),
    (7.0, 104.9, 109.9, 114.9, 119.9, 124.9, 129.9, 134.9),
    (8.0, 108.7, 113.8, 118.9, 124.0, 129.1, 134.2, 139.3),
    (9.0, 112.5, 117.7, 122.9, 128.1, 133.3, 138.5, 143.7),
    (10.0, 116.5, 121.9, 127.3, 132.7, 138.1, 143.5, 148.9),
    (11.0, 120.8, 126.3, 131.8, 137.3, 142.8, 148.3, 153.8),
    (12.0, 125.5, 131.0, 136.5, 142.0, 147.5, 153.0, 158.5),
    (13.0, 129.9, 135.2, 140.5, 145.8, 151.1, 156.4, 161.7),
    (14.0, 132.9, 138.0, 143.1, 148.2, 153.3, 158.4, 163.5),
    (15.0, 134.5, 139.5, 144.5, 149.5, 154.5, 159.5, 164.5),
    (16.0, 135.0, 140.0, 145.0, 150.0, 155.0, 160.0, 165.0),
    (17.0, 135.2, 140.2, 145.2, 150.2, 155.2, 160.2, 165.2),
    (18.0, 135.3, 140.3, 145.3, 150.3, 155.3, 160.3, 165.3),
]

region_corrections = {
    'UKR': 0.0,
    'PL': -2.0,
    'TU': -1.0,
    'JA': -3.0,
    'USA': +1.5
}


def random_graph(request, ditina_id):
    try:
        ditina = Ditina.objects.get(id=ditina_id)
        component_age = float(ditina.vik)
        component_height = float(ditina.zrist)
        user_name = f"{ditina.imya} {ditina.prizvische}".strip()
        region = ditina.region or 'UKR'
        plec = ditina.plec
    except (Ditina.DoesNotExist, ValueError, TypeError) as e:
        logger.error(f"Błąd pobierania danych dziecka: {e}")
        component_age = None
        component_height = None
        user_name = 'Twoje dziecko'
        region = 'UKR'
        plec = 'M'

    correction = region_corrections.get(region, 0.0)
    logger.debug(f"Region: {region}, Correction: {correction}, Płeć: {plec}")

    if plec == 'K':
        selected_base_data = base_data_female
        title_plec = 'Dziewczynki'
    else:
        selected_base_data = base_data_male
        title_plec = 'Chłopcy'

    ages = [x[0] for x in selected_base_data]

    curves = {
        '-3СВ': [round(x[1] + correction, 2) for x in selected_base_data],
        '-2СВ': [round(x[2] + correction, 2) for x in selected_base_data],
        '-1СВ': [round(x[3] + correction, 2) for x in selected_base_data],
        'Średnia': [round(x[4] + correction, 2) for x in selected_base_data],
        '+1СВ': [round(x[5] + correction, 2) for x in selected_base_data],
        '+2СВ': [round(x[6] + correction, 2) for x in selected_base_data],
        '+3СВ': [round(x[7] + correction, 2) for x in selected_base_data],
    }

    style_map = {
        '-3СВ': ('#999999', 'dot'),
        '-2СВ': ('#ff9900', 'dot'),
        '-1СВ': ('#cc0000', 'dot'),
        'Średnia': ('#1f77b4', 'solid'),
        '+1СВ': ('#2ca02c', 'dot'),
        '+2СВ': ('#17becf', 'dot'),
        '+3СВ': ('#9467bd', 'dot'),
    }

    data = []
    for label, values in curves.items():
        color, dash = style_map[label]
        trace = go.Scatter(
            x=ages,
            y=values,
            mode='lines',
            name=label,
            line=dict(color=color, width=2, dash=dash)
        )
        data.append(trace)

    if component_age is not None and component_height is not None:
        data.append(go.Scatter(
            x=[component_age],
            y=[component_height],
            mode='markers',
            marker=dict(size=16, color='#e83e8c', line=dict(width=2, color='black')),
            name=user_name,
            hoverinfo='skip'
        ))

    layout = go.Layout(
        title=f'Wykres: Wiek — Wzrost ({title_plec}) z krzywymi normatywnymi',
        xaxis=dict(title='Wiek (lata)', dtick=1, range=[0, 18]),
        yaxis=dict(title='Wzrost (cm)'),
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        legend=dict(font=dict(size=12)),
        margin=dict(l=60, r=30, t=60, b=60),
    )

    fig = go.Figure(data=data, layout=layout)
    graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    ai_message = ""
    if component_age is not None and component_height is not None:
        try:
            age_years = float(component_age)
        except (ValueError, TypeError):
            ai_message = "<b>Błąd:</b> Nieprawidłowy format wieku. Proszę wprowadzić wartość numeryczną."
            return render(request, 'random_graph.html',
                          {'graph_html': mark_safe(graph_html), 'ai_message': mark_safe(ai_message)})

        if getattr(ditina, 'pryimaie_gormony', False):
            ai_message += (
                "<b>Uwaga:</b> Dziecko przyjmuje preparaty hormonalne. Może to znacząco wpływać na wzrost i rozwój. <b>Obowiązkowo skonsultuj się z lekarzem</b> w celu indywidualnej oceny i regularnego monitorowania.<br><br>")

        closest = min(selected_base_data, key=lambda x: abs(x[0] - age_years))

        expected_height = round(closest[4] + correction, 1)
        delta = component_height - expected_height
        threshold = 7.0

        if delta < -threshold:
            ai_message += (
                f"<b>⚠️ Wzrost poniżej średniej</b> dla dziecka w Twoim wieku ({component_height} cm przy {age_years} latach). Oczekiwana wartość: {expected_height:.1f} cm. <b>Zaleca się kontakt z pediatrą</b> w celu konsultacji i oceny rozwoju.")
        elif -threshold <= delta < -3:
            ai_message += (
                f"<b>Wzrost na dolnej granicy normy</b>: {component_height} cm przy {age_years} latach. Oczekiwany średni wzrost: {expected_height:.1f} cm. <b>Obserwuj dynamikę</b> wzrostu dziecka w ciągu najbliższych miesięcy.")
        elif delta > threshold:
            ai_message += (
                f"<b>Wzrost powyżej średniej</b> dla dziecka w Twoim wieku ({component_height} cm przy {age_years} latach). Oczekiwana wartość: {expected_height:.1f} cm. Może to być cecha indywidualna. Zaleca się <b>okresową obserwację</b>.")
        else:
            ai_message += (
                f"<b>✅ Wzrost w granicach normy</b>: {component_height} cm przy {age_years} latach. Średnia wartość: {expected_height:.1f} cm.")

    else:
        missing_data = []
        if component_age is None: missing_data.append("wiek")
        if component_height is None: missing_data.append("wzrost")
        if missing_data:
            ai_message = (
                f"<b>Brak wystarczających danych do analizy.</b> Proszę wprowadzić: {', '.join(missing_data)}.")
        else:
            ai_message = "Brak wystarczających danych do analizy (nieznana przyczyna)."

    return render(request, 'random_graph.html', {
        'graph_html': mark_safe(graph_html),
        'ai_message': mark_safe(ai_message)
    })