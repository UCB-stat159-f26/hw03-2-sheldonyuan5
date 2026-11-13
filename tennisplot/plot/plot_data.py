import matplotlib.pyplot as plt

COLORS = {"Won": "skyblue", "Lost": "purple"}
REQUIRED_COLUMNS = {"player", "result", "player_age", "age_difference"}

def plot_career_matches(career):
    _check_columns(career)
    colors = career["result"].map(COLORS)
    ax = career.plot.scatter(x="player_age", y="age_difference", c=colors, figsize=(12, 7), s=22, alpha=0.75, zorder=3)
    _style_x_axis(ax, career["player_age"])
    _style_y_axis(ax)
    _add_title_and_legend(ax.figure, career["player"].iloc[0], career["player_age"])
    return ax.figure

def _check_columns(career):
    missing = REQUIRED_COLUMNS - set(career.columns)
    if missing:
        raise ValueError(f"career is missing columns {sorted(missing)}; "
                         "create it with get_career_matches()")

def _style_x_axis(ax, ages):
    youngest, oldest = int(ages.min()), int(ages.max()) + 1
    ax.set_xlim(youngest - 0.5, oldest + 0.5)
    ax.set_xticks(range(youngest, oldest + 1, 2))
    ax.tick_params(axis="x", top=True, labeltop=True, bottom=False, labelbottom=False)
    ax.set_xlabel("")

def _style_y_axis(ax):
    ax.set_yticks([-20, -10, 0, 10, 20], ["\u221220", "\u221210", "Same age", "+10", "+20 years"])
    ax.set_ylabel("")
    ax.grid(True, color="lightgray", linewidth=0.8, zorder=0)
    ax.axhline(0, color="dimgray", linewidth=1, zorder=2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, labelsize=11)

def _add_title_and_legend(fig, player, ages):
    title = f"{player}\u2019s Professional Matches, Age {int(ages.min())} to {int(ages.max())}"
    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.995)
    last_name = player.split()[-1]
    labels = {"Won": f"Match {last_name} won", "Lost": "Match lost"}
    legend = [_legend_dot(COLORS[key], labels[key]) for key in COLORS]
    fig.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.955), ncol=2, fontsize=12, handletextpad=0.3, frameon=False)
    fig.subplots_adjust(top=0.80, bottom=0.04, left=0.08, right=0.98)

def _legend_dot(color, label):
    return plt.Line2D([], [], marker="o", linestyle="", markersize=8,
                      color=color, label=label)
    