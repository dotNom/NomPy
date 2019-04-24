import plotly.offline as py
import plotly.graph_objs as go
import math as m
import textwrap
import pandas as pd

def plotMap(events,mapbox_access_token):
    
    if mapbox_access_token == 0:
        tableOnly = True
    
    tableData = {'Event Name':[],'Date':[],'Time':[],'Location':[]}
    csvData = {'Event Name':[],'Date':[],'Time':[],'Location':[],'Link':[]}
    def Listattributes(event):
        if hasattr(event, 'title'):
            date = event.title.split(': ')[0]
            if hasattr(event, 'link'):
                titleText = '<a href="' + event.link + '">' + event.title.split(date)[1][2:] +'</a>'
                tableData['Event Name'].append(titleText)
                csvData['Link'].append(event.link)
            else:
                tableData['Event Name'].append(event.title.split(date)[1][2:])
            tableData['Date'].append(date)
            csvData['Event Name'].append(event.title.split(date)[1][2:])
        else:
            tableData['Event Name'].append('')
            csvData['Event Name'].append('')
            tableData['Date'].append('')
            
        if hasattr(event, 'locwithBUI'):
            tableData['Location'].append(event.locwithBUI.split('LOCATION:')[1].replace('\\',''))
        else:
            tableData['Location'].append('')
            
        if hasattr(event, 'timestr'):
            tableData['Time'].append(event.timestr)
        else:
            tableData['Time'].append('')
            
#        if hasattr(event, 'link'):
#            linkText = '<a href="' + event.link + '">Link to Event</a>'
#            tableData['Link'].append(linkText)
#        else:
#            tableData['Link'].append('')
            
    csvData['Date'] = tableData['Date']        
    csvData['Time'] = tableData['Time']        
    csvData['Location'] = tableData['Location']        
    mapData = []
    lat = []
    lon = []
    text = []
    geocount = 0
    hours = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for item in events: 
        timeStr = ''
        if hasattr(item, 'timestart') and hasattr(item,'timeend'): 
            if item.timeend is not None:
                Starttime = item.timestart.split('T')[-1]
                Starttime = Starttime.split('Z')[0]
                Starthour = int(Starttime[0:2])-5
                Starthour = hours[Starthour]
                Startminute = Starttime[2:4]
                Starttime = str(Starthour)+':'+Startminute
                
                Endtime = item.timeend.split('T')[-1]
                Endtime = Endtime.split('Z')[0]
                Endhour = int(Endtime[0:2])-5
                Endhour = hours[Endhour]
                Endminute = Endtime[2:4]
                Endtime = str(Endhour)+':'+Endminute
                
                timeStr = Starttime + '-' + Endtime
            else: 
                if 'VALUE=DATE' in item.timestart:
                    timeStr = 'All Day'
            setattr(item,'timestr',timeStr)
            
        if hasattr(item, 'geo'):
            geocount += 1
            geo1,geo2 = item.geo
            lat.append(geo1)
            lon.append(geo2)
            formatted_text = ''
            if hasattr(item, 'title'):
                wrapper = textwrap.TextWrapper(width=30)
                wrapped_text = wrapper.fill(text=item.title)
                wrapped_text = wrapped_text.replace('\n','<br>')
                formatted_text = 'Event Name:<br>'
                formatted_text += wrapped_text + '<br><br>'
            
            if timeStr:
                formatted_text += 'Time: ' + timeStr + '<br><br>'
                
            text.append(formatted_text)
        Listattributes(item)
                
    if geocount == 0:
        tableOnly = True
    
    centerLat = (max([float(i) for i in lat])+min([float(i) for i in lat]))/2
    centerLon = (max([float(i) for i in lon])+min([float(i) for i in lon]))/2
        
    data = []
    mapData = dict(
            hoverlabel = go.scattermapbox.Hoverlabel(
                    bgcolor='rgb(191,87,0)',
                    bordercolor='rgb(51,63,72)',
                    font=go.scattermapbox.hoverlabel.Font(color='rgb(255,255,255)'),
                    namelength=-1
            ),
            lat = lat,
            lon = lon,
            hoverinfo = 'text',
            marker = go.scattermapbox.Marker(
                    size = 14,
                    symbol='restaurant', 
                ),
            text = text,
            type = 'scattermapbox'
            )
    data.append(mapData)
    
    # Get map area bounded by points and make the map 20% bigger
    actLatDiff = (max([abs(float(i)) for i in lat])-min([abs(float(i)) for i in lat]))*1.2
    actLonDiff = (max([abs(float(i)) for i in lon])-min([abs(float(i)) for i in lon]))*1.2
    
    
    zoomLvls = []
    # Use logrithmic functions to set the zoom level
    if actLatDiff > 0:
        zoomLat = -1.454*m.log(actLatDiff)+8.3928
        zoomLvls.append(zoomLat)
    if actLonDiff > 0:
        zoomLon = -1.452*m.log(actLonDiff)+9.3217
        zoomLvls.append(zoomLon)
    
    if len(zoomLvls) == 0: # Default zoom level
        zoomLvls = [13]
    
    df = pd.DataFrame(tableData)
    df2 = pd.DataFrame(csvData)
    
    plotTable = go.Table(
        columnorder = [1,2,3,4],
        columnwidth = [3,2,2,3],
        domain=dict(x=[0.55, 1.0],
                    y=[0, 1]),
        header=dict(values=['<b>Event Name</b>','<b>Date</b>','<b>Time</b>','<b>Location</b>'],
                    fill = dict(color='#C2D4FF'),
                    align = ['left'] * 5),
        cells=dict(values=[df['Event Name'],df.Date,df.Time,df.Location],
                   fill = dict(color='#F5F8FF'),
                   align = ['left'] * 5))
    
    data.append(plotTable)   
    
    layout = dict(
        width=1500,
        height=800,
        autosize=False,
        title='<b>Free Food Events</b>',
        margin = dict(t=100),
        showlegend=False            
        )
    
    if tableOnly:   
        plotTable.domain=dict(x=[0, 1.0],y=[0, 1])
        fig = dict(data=[plotTable], layout=layout)
    else:
        layout['mapbox']=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=centerLat,
                    lon=centerLon
                ),
                pitch=0,         
                zoom = min(zoomLvls),
                domain=dict(x=[0, 0.53],
                        y=[0, 1.0]))    
        fig = dict(data=data, layout=layout)
    
    df2.to_csv(r'Free_Food_Events.csv',index = False)
    py.plot(fig, filename='Find_Free_Food.html')
    
#if __name__ == '__main__':
#    plotMap(foodEvents,mapbox_access_token)