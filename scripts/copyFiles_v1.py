import os
import time
from pip._internal import main as pipmain
import pandas as pd
from bokeh.models import (ColumnDataSource, HoverTool, LabelSet, ranges)
from bokeh.models.formatters import PrintfTickFormatter
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import SingleIntervalTicker, LinearAxis
from bokeh.layouts import column


# File Locations
file_source = "/Users/navdsharma/Documents/03_Manilla_GDC/Scripts/data/src/source_file.txt"
file_destination = "~/dummy/"
pem_location = "/Users/navdsharma/Downloads/SydneyJKVWebSite.pem"
destination_machine = "ubuntu@ec2-54-79-95-26.ap-southeast-2.compute.amazonaws.com"

# File Size in bytes
file_size = 1000000

# File Transfer Rate and Duration in seconds
file_transfer_rate = 10
duration = 300


# FUNCTION - Installs the given Module in Python
def install(package):
    pipmain(['install', package])


# FUNCTION - Create Source file of given size
def create_source_file(given_file_size, source_file_location):
    with open(source_file_location, "wb") as f:
        f.write(os.urandom(given_file_size))

    print("Source File Created...")


# FUNCTION - File Transfer at given rate
def file_transfer_at_given_rate(total_duration, rate_of_file_transfer):
    # Message
    print("File Transfer Rate is - 1 File of {} MB every {} seconds".format(file_size/1000000, rate_of_file_transfer))

    print("Based on given duration ({} secs) and File Transfer Rate as mentioned above, "
          "{} file transfers would be attempted...".format(total_duration, total_duration // rate_of_file_transfer))

    # Create Dataframe
    results_df = pd.DataFrame(columns=["Start_Time", "File_Number", "Transfer_Time"])

    # Transfer files
    for file_number in range(total_duration // rate_of_file_transfer):
        current_time = time.strftime("%H:%M:%S")
        start_time = time.perf_counter()
        os.system("scp -i {} -r {} {}:{}".format(pem_location, file_source, destination_machine, file_destination))
        transfer_time = time.perf_counter() - start_time

        print("File_{} transfer started at {} and got completed in {} secs...".format(file_number+1, start_time,
                                                                                      round(transfer_time, 3)))

        # Adding to dataframe
        results_df.loc[file_number] = [current_time, file_number+1, transfer_time]

        # Sleep
        if file_transfer_rate-transfer_time < 0:
            time.sleep(5)
        else:
            time.sleep(file_transfer_rate-transfer_time)

    # Set correct datatypes
    results_df['Start_Time'] = results_df['Start_Time'].astype('datetime64[ns]')
    results_df['File_Number'] = results_df['File_Number'].astype(int)

    # Save Dataframe to csv
    results_file_name = "Results_" + time.strftime("%H%M%S") + ".csv"
    results_df.to_csv(results_file_name, sep=',', index=False)
    print("Raw Results File generated! Please check file - {}".format(results_file_name))

    return results_df


# FUNCTION - Set the properties of the hover tool tips.
def set_hover_tool_tips_graph1() -> object:
    hover_tool_tips = HoverTool(
        tooltips=[
            ("Time Taken", "@Transfer_Time{0.2f} secs")
        ],

        formatters={'@Transfer_Time': 'printf'},

        mode='mouse'  # display a tooltip whenever the cursor is vertically in line with a glyph
    )

    return hover_tool_tips


# FUNCTION - Set the properties of the hover tool tips.
def set_hover_tool_tips_graph2() -> object:
    hover_tool_tips = HoverTool(
        tooltips=[
            ("Time Taken", "@values{0.2f} secs")
        ],

        formatters={'@values': 'printf'},

        mode='mouse'  # display a tooltip whenever the cursor is vertically in line with a glyph
    )

    return hover_tool_tips


# FUNCTION - Sets the Properties of the graph and the legend of the graph
def set_graph_and_legend_properties(plot_graph: figure(), graph_title: str) -> figure():

    # X-Axis related formatting
    plot_graph.xgrid.grid_line_color = "white"
    plot_graph.xgrid.grid_line_dash = [6, 4]
    plot_graph.xgrid.grid_line_alpha = .3
    plot_graph.xaxis.axis_line_color = "white"
    plot_graph.xaxis.axis_label_text_color = "white"
    plot_graph.xaxis.major_label_text_color = "white"
    plot_graph.xaxis.major_tick_line_color = "white"
    plot_graph.xaxis.minor_tick_line_color = "white"

    # Y-axis related formatting
    plot_graph.ygrid.grid_line_color = "white"
    plot_graph.ygrid.grid_line_dash = [6, 4]
    plot_graph.ygrid.grid_line_alpha = .3
    plot_graph.yaxis.axis_line_color = "white"
    plot_graph.yaxis.axis_label_text_color = "white"
    plot_graph.yaxis.major_label_text_color = "white"
    plot_graph.yaxis.major_tick_line_color = "white"
    plot_graph.yaxis.minor_tick_line_color = "white"

    # Graph related Formatting
    plot_graph.min_border_left = 80
    plot_graph.title.text = graph_title
    plot_graph.title.text_color = "white"
    plot_graph.title.text_font = "times"
    plot_graph.title.text_font_style = "normal"
    plot_graph.title.text_font_size = "14pt"
    plot_graph.title.align = "center"
    plot_graph.background_fill_color = '#2F2F2F'
    plot_graph.border_fill_color = '#2F2F2F'
    plot_graph.outline_line_color = '#444444'

    return plot_graph


# FUNCTION - Creates graph based on the dataframe
def create_graph(results_df):
    # Plot 1st Graph
    source = ColumnDataSource(results_df)

    transfer_rate_time_graph = figure(x_axis_label="Files",
                                      x_axis_type=None,
                                      y_axis_label="Time Taken to Transfer File(secs)",
                                      toolbar_location="below",
                                      tools="save")

    # Ticker Props
    ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
    xaxis = LinearAxis(ticker=ticker)
    transfer_rate_time_graph.add_layout(xaxis, 'below')

    # Bar Graph
    transfer_rate_time_graph.vbar(x='File_Number',
                                  top="Transfer_Time",
                                  bottom=0,
                                  source=source,
                                  width=0.3,
                                  color="#FFBF00")

    # Line Graph
    transfer_rate_time_graph.line(x='File_Number',
                                  y="Transfer_Time",
                                  source=source,
                                  line_width=2,
                                  color="#FFFF00")

    # Format axises
    transfer_rate_time_graph_final = set_graph_and_legend_properties(transfer_rate_time_graph,
                                                                     "Transfer Rate Time (sec)")

    # Add Tool - Hovertool
    transfer_rate_time_graph_final.add_tools(set_hover_tool_tips_graph1())

    # Format x-axis labels
    transfer_rate_time_graph_final.xaxis.formatter = PrintfTickFormatter(format="File_%1.0f")

    # Plot 2nd Graph
    # Create Data Source
    y_axis = ['Min', 'Avg', 'Max', '90th', '95th', '99th']
    x_axis = [round(results_df['Transfer_Time'].min(), 2),
              round(results_df['Transfer_Time'].mean(), 2),
              round(results_df['Transfer_Time'].max(), 2),
              round(results_df['Transfer_Time'].quantile(0.90), 2),
              round(results_df['Transfer_Time'].quantile(0.95), 2),
              round(results_df['Transfer_Time'].quantile(0.99), 2)]

    # Create Source
    graph2_source = ColumnDataSource(dict(y=y_axis, right=x_axis))

    # Write results to csv
    aggregate_results_df = pd.DataFrame.from_dict(dict(Metrics=y_axis, Value=x_axis))

    # Save Dataframe to csv
    agg_report_name = "Perf_Summary_" + time.strftime("%H%M%S") + ".csv"
    aggregate_results_df.to_csv(agg_report_name, sep=',', index=False)

    print("Performance Metrics Summary report generated!. Please check file - {}".format(agg_report_name))

    # Create Fig
    aggregates_graph = figure(y_range=y_axis,
                              x_range=ranges.Range1d(start=0, end=results_df['Transfer_Time'].max() + 0.4),
                              toolbar_location=None,
                              tools="save")

    # Add Labels
    labels = LabelSet(x='right',
                      y='y',
                      text='right',
                      source=graph2_source,
                      level='glyph',
                      x_offset=5,
                      y_offset=5,
                      render_mode='canvas',
                      text_color='white')

    # Create hBar
    aggregates_graph.hbar(y='y',
                          right='right',
                          source=graph2_source,
                          left=0,
                          height=0.5)

    # Format axises and add labels
    aggregates_graph_final = set_graph_and_legend_properties(aggregates_graph, "Performance Metrics (secs)")
    aggregates_graph_final.add_layout(labels)

    # output to static HTML file
    graph_file_name = "perf_test_report_" + time.strftime("%H%M%S") + ".html"
    output_file(graph_file_name)

    # Save Graph
    save(column(transfer_rate_time_graph_final, aggregates_graph_final))

    # Success Message
    print("Graph generated successfully! Please check file - {}".format(graph_file_name))


# Start
if __name__ == '__main__':
    print("Script Started...")
    # Start Time of Code
    start_time = time.time()

    # Create Source File
    create_source_file(file_size, file_source)

    # Transfer files
    source_graph_df = file_transfer_at_given_rate(duration, file_transfer_rate)

    # Create Graph
    create_graph(source_graph_df)

    # Print Time taken to execute script
    print("CUSTOM INFO : --- Script Execution Time: %s seconds ---" % (time.time() - start_time))




