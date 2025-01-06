import pandas as pd
from matplotlib import pyplot as plt
# xml library
import xml.dom.minidom as minidom

from livingLab.util.experiment_constants import START_MORNING_WORK, FINISH_MORNING_WORK, START_AFTERNOON_WORK, \
    FINISH_AFTERNOON_WORK


# read trace.xml



def runReport():
    traces = []
    #<HumanState><current_time>465.0</current_time><luminance>25024.46389394153</luminance><artificial_light_state><luminance_output>0</luminance_output></artificial_light_state><blinds_closed>false</blinds_closed><artificial_light_on>false</artificial_light_on><window_light_state><luminance_output>41706.74471082404</luminance_output></window_light_state></HumanState><?xml version="1.0" encoding="utf-8"?>

    brightnessSensor = []

    with open("trace.xml", "r") as f:
        for line in f:
            if "<HumanState>" in line:
                traces.append(line)
            if "<BrightnessState>" in line:
                brightnessSensor.append(line)

    # parse traces
    df = pd.DataFrame(columns=["time", "luminance","al_luminance","window_luminance", "artificial_light_on", "blinds_closed"])

    for i in range(len(traces)):
        trace = traces[i]
        bs = brightnessSensor[i]
        df = df.append({
            "time": float(minidom.parseString(trace).getElementsByTagName("current_time")[0].firstChild.nodeValue),
            "luminance": float(minidom.parseString(trace).getElementsByTagName("luminance")[0].firstChild.nodeValue),
            "al_luminance": float(minidom.parseString(trace).getElementsByTagName("artificial_light_state")[0].getElementsByTagName("luminance_output")[0].firstChild.nodeValue),
            "window_luminance": float(minidom.parseString(trace).getElementsByTagName("window_light_state")[0].getElementsByTagName("luminance_output")[0].firstChild.nodeValue),
            "artificial_light_on": minidom.parseString(trace).getElementsByTagName("artificial_light_on")[0].firstChild.nodeValue,
            "blinds_closed": minidom.parseString(trace).getElementsByTagName("blinds_closed")[0].firstChild.nodeValue,
            "brightnessSensor": float(minidom.parseString(bs).getElementsByTagName("luminance")[0].firstChild.nodeValue)
        }, ignore_index=True)

    # plot
    plt.plot(df["time"], df["luminance"], label="human_perceived_luminance")
    plt.plot(df["time"], df["window_luminance"], label="window_luminance")
    # transparent line
    plt.plot(df["time"], df["al_luminance"], label="al_luminance", color="red")

    # draw a line at start work time
    plt.axvline(x=START_MORNING_WORK, color="black", linestyle="--", label="WORK_START")
    plt.axvline(x=FINISH_AFTERNOON_WORK, color="black", linestyle="--", label="WORK_FINISH")

    # add brightness sensor
    plt.plot(df["time"], df["brightnessSensor"], label="sensor_perceived_luminance", color="green")

    # only show from work start to work finish
    plt.xlim(START_MORNING_WORK-60, FINISH_AFTERNOON_WORK+120)

    # show axis labels
    plt.xlabel("Time (minutes)")
    plt.ylabel("Luminance (lux)")

    # show labels in legend at top right
    plt.legend(loc="upper right")
    plt.show()
