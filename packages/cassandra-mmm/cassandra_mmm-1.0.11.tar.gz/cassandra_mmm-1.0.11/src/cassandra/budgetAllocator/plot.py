import plotly.graph_objects as go


def show_budget_allocator(df_budget_allocator):
    fig_spend = go.Figure()

    fig_spend.add_bar(x=round(df_budget_allocator['actual_spend'], 2), y=df_budget_allocator['canale'], orientation='h',
                      name='Actual Spend',
                      marker=dict(color="Purple"))
    fig_spend.add_bar(x=round(df_budget_allocator['optimal_spend'], 2), y=df_budget_allocator['canale'],
                      orientation='h', name='Optimal Spend',
                      marker=dict(color="MediumPurple"))

    fig_spend.update_layout(
        xaxis_title='Spesa',
        yaxis_title='Canale',
        title='Actual Spend vs Optimal Spend')

    fig_spend.show()

    fig_response = go.Figure()

    fig_response.add_bar(x=round(df_budget_allocator['actual_response'], 2), y=df_budget_allocator['canale'],
                         orientation='h', name='Actual Response',
                         marker=dict(color="Purple"))
    fig_response.add_bar(x=round(df_budget_allocator['optimal_response'], 2), y=df_budget_allocator['canale'],
                         orientation='h', name='Optimal Response',
                         marker=dict(color="MediumPurple"))

    fig_response.update_layout(
        xaxis_title='Response',
        yaxis_title='Canale',
        title='Actual Response vs Optimal Response')

    fig_response.show()
