import typer
from typer import Option
from typing import Optional
from thingsmatrix import apis
from rich.console import Console

app = typer.Typer()
api = apis.ThingsMatrix()
console = Console()


@app.command()
def reports(sn: Optional[str] = typer.Argument(..., help='imei'),
            starttime: Optional[str] = typer.Option(
                None, help='Format as YYYY-mm-dd HH:mm:ss'),
            endtime: Optional[str] = typer.Option(
                None, help='Format as YYYY-mm-dd HH:mm:ss')):
    '''
    Filter reports by imei and datetime
    '''
    response, reports = api.get_devices_reports(sn=sn,
                                                startTime=starttime,
                                                endTime=endtime)
    if response != None or reports != None:
        console.print(response.json()['data']['content'])


# @app.command()
# def devices(sn:Optional[str],model:Optional[str],group:Optional[str],status:Optional[str]):
#     api.get_devices()


@app.command()
def device(sn: str,
           status: bool = Option(
               False,
               "--status",
               "-s",
               help="show status",
           ),
           model: bool = Option(
               False,
               "--model",
               "-m",
               help="show model name",
           ),
           group: bool = Option(
               False,
               "--group",
               "-g",
               help="show group name",
           ),
           location_mode: bool = Option(
               False,
               "--location_mode",
               "-lm",
               help="show location mode",
           ),
           heartbeat: bool = Option(
               False,
               "--heatbeat",
               "-hb",
               help="show heartbeat timer setting",
           ),
           ac_report_interval: bool = Option(
               False,
               "--ac_report_interval",
               "-ari",
               help="show ac report interval",
           ),
           dc_report_interval: bool = Option(
               False,
               "--dc_report_interval",
               "-dri",
               help="show dc report interval",
           ),
           gps_report_interval: bool = Option(
               False,
               "--gps_report_interval",
               "-gri",
               help="show gps report interval",
           )):
    '''
    Get device by serial number
    '''
    device = api.get_device(sn)
    if device:
        if status:
            console.print(device.status.name)
        elif model:
            console.print(device.model.name)
        elif group:
            console.print(device.group.name)
        elif location_mode:
            console.print(device.latest.gpsLocating.name)
        elif heartbeat:
            console.print(device.template.heartbeat_timer)
        elif ac_report_interval:
            console.print(device.template.ac_report_interval)
        elif dc_report_interval:
            console.print(device.template.dc_report_interval)
        elif gps_report_interval:
            console.print(device.template.gps_report_interval)
        else:
            device.printJson()


def run():
    try:
        app()
        typer.Exit(0)
    except Exception as e:
        print(e)
        typer.Exit(-1)


if __name__ == "__main__":
    try:
        app()
        typer.Exit(0)
    except Exception as e:
        print(e)
        typer.Exit(-1)
