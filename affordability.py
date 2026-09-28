import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Voter Affordability Sentiment", layout="centered")


def create_affordability_chart():
  categories = [
      'Education',
      'Housing',
      'Health care',
      'Having a family',
      'Groceries',
      'Food',
      'Utilities',
      'Transportation',
  ]

  unaffordable = [58, 54, 47, 44, 28, 26, 23, 22]
  somewhat = [26, 31, 37, 38, 54, 59, 57, 47]
  mostly = [8, 13, 13, 13, 17, 14, 19, 28]

  # Calculate remainder percentage (grey category separator slivers)
  remainder = [
      100 - (u + s + m) for u, s, m in zip(unaffordable, somewhat, mostly)
  ]

  df = pd.DataFrame({
      'Category': categories,
      'Unaffordable': unaffordable,
      'Other/No Answer': remainder,
      'Somewhat Affordable': somewhat,
      'Mostly Affordable': mostly,
  }).sort_values('Unaffordable', ascending=True)

  # Custom y-positions with Education offset at top
  y_positions = np.array([0, 1, 2, 3, 4, 5, 6, 7.5])
  height = 0.65

  fig, ax = plt.subplots(figsize=(10, 7.2), dpi=300)

  # Muted color palette
  c_unaffordable = '#E08A5D'  # Faded Orange
  c_other = '#A0A0A0'  # Medium Grey
  c_somewhat = '#C2E2C2'  # Faded Light Green
  c_mostly = '#669E68'  # Faded Dark Green

  # Stacked horizontal bars
  bars1 = ax.barh(
      y_positions, df['Unaffordable'], height=height, color=c_unaffordable
  )
  bars2 = ax.barh(
      y_positions,
      df['Other/No Answer'],
      left=df['Unaffordable'],
      height=height,
      color=c_other,
  )
  bars3 = ax.barh(
      y_positions,
      df['Somewhat Affordable'],
      left=df['Unaffordable'] + df['Other/No Answer'],
      height=height,
      color=c_somewhat,
  )
  bars4 = ax.barh(
      y_positions,
      df['Mostly Affordable'],
      left=df['Unaffordable']
      + df['Other/No Answer']
      + df['Somewhat Affordable'],
      height=height,
      color=c_mostly,
  )

  # Y-axis category labels
  ax.set_yticks(y_positions)
  ax.set_yticklabels(
      df['Category'], fontsize=11, color='black', fontweight='normal'
  )

  # Hide chart border spines, grid, and x-axis ticks
  for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

  ax.grid(False)
  ax.xaxis.set_visible(False)
  ax.tick_params(axis='y', which='both', length=0, labelsize=11)

  # Annotations inside bars (non-bold text)
  for idx, (b1, b2, b3, b4) in enumerate(zip(bars1, bars2, bars3, bars4)):
    w1, w2, w3, w4 = (
        b1.get_width(),
        b2.get_width(),
        b3.get_width(),
        b4.get_width(),
    )
    y = b1.get_y() + b1.get_height() / 2
    category_name = df['Category'].iloc[idx]

    pct = '%' if category_name == 'Education' else ''

    if w1 > 5:
      ax.text(
          w1 / 2,
          y,
          f'{int(w1)}{pct}',
          va='center',
          ha='center',
          fontsize=9,
          fontweight='normal',
          color='black',
      )
    if w3 > 5:
      ax.text(
          w1 + w2 + w3 / 2,
          y,
          f'{int(w3)}{pct}',
          va='center',
          ha='center',
          fontsize=9,
          fontweight='normal',
          color='black',
      )
    if w4 > 5:
      ax.text(
          w1 + w2 + w3 + w4 / 2,
          y,
          f'{int(w4)}{pct}',
          va='center',
          ha='center',
          fontsize=9,
          fontweight='normal',
          color='black',
      )

  # Section headers with category color matching
  top_bar_unaff = bars1[-1]
  top_y_above = top_bar_unaff.get_y() + top_bar_unaff.get_height() + 0.15
  ax.text(
      0,
      top_y_above,
      'UNAFFORDABLE',
      fontsize=10,
      fontweight='bold',
      color=c_unaffordable,
      va='bottom',
      ha='left',
  )

  top_bar_somewhat = bars3[-1]
  top_x_somewhat = top_bar_somewhat.get_x()
  top_y_below = top_bar_somewhat.get_y() - 0.20
  ax.text(
      top_x_somewhat,
      top_y_below,
      'SOMEWHAT\nAFFORDABLE',
      fontsize=10,
      fontweight='bold',
      color=c_somewhat,
      va='top',
      ha='left',
      linespacing=1.1,
  )

  top_bar_mostly = bars4[-1]
  ax.text(
      100,
      top_y_above,
      'MOSTLY\nAFFORDABLE',
      fontsize=10,
      fontweight='bold',
      color=c_mostly,
      va='bottom',
      ha='right',
      linespacing=1.1,
  )

  ax.set_xlim(0, 100)
  ax.set_ylim(-0.5, 9.2)

  # Non-bold title with left edge aligned at x=0
  title_text = "Voters' feelings about the\naffordability of the following items"
  ax.text(
      0,
      8.4,
      title_text,
      fontsize=14,
      fontweight='normal',
      color='black',
      va='bottom',
      ha='left',
      linespacing=1.2,
  )

  plt.tight_layout()
  return fig


# Render in Streamlit interface
fig = create_affordability_chart()
st.pyplot(fig, use_container_width=True)
