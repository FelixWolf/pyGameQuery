import varformat
import http.server
import time
import cgi
from pyGameQuery import source

ServerAddr = ("0.0.0.0", 1234)

template = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="525" height="80">
  <style type="text/css">
  <![CDATA[
    .text{
        font-size:12px;
        font-style:normal;
        font-weight:normal;
        line-height:125%;
        letter-spacing:0px;
        word-spacing:0px;
        fill:#000000;
        fill-opacity:1;
        stroke:none;
        filter:url(#text_shadow);
        font-family:Sans;
    }
    .text tspan{
        font-size:12px;
        font-style:normal;
        font-variant:normal;
        font-weight:normal;
        font-stretch:normal;
        text-align:start;
        line-height:125%;
        letter-spacing:-1px;
        writing-mode:lr-tb;
        text-anchor:start;
        font-family:Monospace;
    }
    #graph path{
        fill:none;
        stroke:#888888;
        stroke-width:1px;
        stroke-linecap:butt;
        stroke-linejoin:miter;
        stroke-opacity:1;
    }
    #graph_text text{
        font-size:40px;
        font-style:normal;
        font-weight:normal;
        line-height:125%;
        letter-spacing:0px;
        word-spacing:0px;
        fill:#000000;
        fill-opacity:1;
        stroke:none;
        font-family:Sans;
    }
    #graph_text text tspan{
        font-size:8px;
    }
    #graph_text text[id^=scale_]{
        text-align:end;
        text-anchor:end;
    }
  ]]>
  </style>
  <defs>
    <linearGradient id="bg_grad_src">
      <stop style="stop-color:#486a9b;stop-opacity:1" offset="0" />
      <stop style="stop-color:#ccdbf1;stop-opacity:1" offset="1" />
    </linearGradient>
    <filter color-interpolation-filters="sRGB" id="text_shadow">
      <feFlood result="f" flood-color="#FCFEFC" flood-opacity="1" />
      <feComposite in2="SourceGraphic" operator="in" in="f" result="c" />
      <feOffset result="o" dy="1" dx="1" />
      <feComposite in2="o" operator="over" in="SourceGraphic" result="c" />
    </filter>
    <clipPath id="graph_clip">
      <rect width="135" height="35" rx="0" ry="0" x="383" y="13" />
    </clipPath>
    <linearGradient x1="0" y1="0" x2="0" y2="80" id="bg_grad"
        xlink:href="#bg_grad_src" gradientUnits="userSpaceOnUse" />
  </defs>
  <g>
    <g id="background">
      <rect width="525" height="80" rx="0" x="0" y="0" id="grad"
         style="fill:url(#bg_grad);fill-opacity:1;stroke:none" />
      <rect width="366" height="19" x="0" y="0" id="bg_name"
         style="fill:#486a9b;fill-opacity:1;stroke:none" />
      <path d="m 365,0 0,80 M 0,0 0,80 525,80 525,0" id="bg_outline"
         style="fill:none;stroke:#486a9b;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none" />
    </g>
    <g id="server_meta">
      <text x="35" y="36" id="server_addr" xml:space="preserve" class="text"><tspan
           x="35" y="36">IP:${SERVER_IP}:${SERVER_PORT}</tspan></text>
      <text x="3" y="52" id="server_player_count" xml:space="preserve" class="text"><tspan
           x="3" y="52">Players:${PLAYERS_CURRENT}/${PLAYERS_MAX}</tspan></text>
      <text x="28" y="68" id="server_map" xml:space="preserve" class="text"><tspan
           x="28" y="68">Map:${MAP_NAME}</tspan></text>
      <text x="202" y="36" id="server_geo" xml:space="preserve" class="text"><tspan
           x="202" y="36">Location:${SERVER_GEO}</tspan></text>
      <text x="177" y="52" id="server_updated" xml:space="preserve" class="text"><tspan
           x="177" y="52">Last Updated:${TRACKER_REFRESH}</tspan></text>
      <text x="196" y="68" id="tracker_ranking" xml:space="preserve" class="text"><tspan
           x="196" y="68">Game Rank:${TRACKER_RANK}/${TRACKER_TOTAL}</tspan></text>
      <text x="40" y="13" id="server_name" xml:space="preserve" class="text"><tspan
           x="40" y="13">${SERVER_NAME}</tspan></text>
    </g>
    <g id="graph">
      <path id="measure_minor" style="stroke:#888888;"
         d="m 510,46 0,2 m -6,-2 0,2 m -6,-2 0,2 m -10,-2 0,2 m -6,-2 0,2 m -6,-2 0,2 m -11,-2 0,2 m -6,-2 0,2 m -6,-2 0,2 m -10,-2 0,2 m -6,-2 0,2 m -6,-2 0,2 m -11,-2 0,2 m -6,-2 0,2 m -6,-2 0,2 m -10,-2 0,2 m -6,-2 0,2 m -6,-2 0,2"/>
      <path id="measure_major" style="stroke:#000000;" 
         d="m 516,44 0,4 m -23,-4 0,4 m -22,-4 0,4 m -23,-4 0,4 m -22,-4 0,4 m -23,-4 0,4"/>
      <path id="graph_bar" clip-path="url(#graph_clip)" style="stroke:#000000;"
         d="m 382,47 0,0 ${SERVER_POP:len=21;height=34}"/>
      <path id="graph_box" style="stroke:#ffffff;"
         d="m 382,38 136,0 m 0,-8 -136,0 m 0,-8 136,0 m -136,-9 136,0 0,35 -136,0 z"/>
    </g>
    <g id="graph_text">
      <text x="421" y="10" id="info_last24" xml:space="preserve"><tspan
           x="421" y="10">Last 24 Hours</tspan></text>
      <text x="385" y="57" id="time_scale" xml:space="preserve"><tspan
           x="385" y="57">12pm 4am 8am 12am 4pm 8pm</tspan></text>
      <text x="380" y="17" id="scale_top" xml:space="preserve"><tspan
           x="380" y="17">28</tspan></text>
      <text x="380" y="25" id="scale_high" xml:space="preserve"><tspan
           x="380" y="25">21</tspan></text>
      <text x="380" y="33" id="scale_low" xml:space="preserve"><tspan
           x="380" y="33">14</tspan></text>
      <text x="380" y="41" id="scale_bot" xml:space="preserve"><tspan
           x="380" y="41">7</tspan></text>
    </g>
    <image x="24" y="2" width="14" height="14" id="server_game_icon" 
       xlink:href="${ICON_GAME}"/>
    <image x="16" y="26" width="16" height="11" id="server_geo_flag" 
       xlink:href="${ICON_GEO}"/>
  </g>
</svg>"""

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        """Respond to a GET request."""
        if s.path[:8] == "/banner/":
            req = s.path[8:].split(":", 1)
            if len(req) > 1:
                req[1] = int(req[1])
            else:
                req.append(27015)
            res = None
            try:
                q = source.sourceQueryInfo(req[0], req[1])
                res = q.get()
            except:
                s.send_response(500)
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                s.wfile.write(b"error")
            else:
                s.send_response(200)
                s.send_header("Content-type", "image/svg+xml")
                s.end_headers()
                test = varformat.format({
                    "SERVER_IP": cgi.escape(req[0]),
                    "SERVER_PORT": req[1],
                    "PLAYERS_CURRENT": res.get("Players", 0),
                    "PLAYERS_MAX": res.get("Max_Players", 0),
                    "MAP_NAME": cgi.escape(res.get("Map", "Unknown")),
                    "SERVER_GEO": res.get("?", "Unknown"),
                    "TRACKER_REFRESH": "Just now",
                    "TRACKER_RANK": 0,
                    "TRACKER_TOTAL": 0,
                    "SERVER_NAME": cgi.escape(res.get("Name", "Unknown")),
                    "SERVER_POP": "",
                    "TRACKER_RANK": 0,
                    "ICON_GAME": "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs=",
                    "ICON_GEO": "data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs="
                })
                s.wfile.write(test.format(template).encode())
        else:
            s.send_response(200)
            s.send_header("Content-type", "text/plain")
            s.end_headers()
            s.wfile.write(b"See: http://host/banner/<IP | host>[:Port]")
            
if __name__ == '__main__':
    server_class = http.server.HTTPServer
    httpd = server_class(ServerAddr, MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % ServerAddr)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % ServerAddr)

