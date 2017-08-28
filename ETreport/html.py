
def html(date,header,bodies):

    headers = header
    output_bodies = bodies
    html_temp = """
    <style type="text/css">
    <!--
    table.t1 {
    border-width: 1px 0 0 1px;
    border-style: solid;
    border-color: #666;
    }
    table.t1 td{
    border-width: 0 1px 1px 0;
    border-style: solid;
    border-color: #666;
    font:Arial;
    text-align:center;
    }
    table.t1 td.highlight{
    font-color:red;
    background-color:yellow;
    }
    -->
    </style>

    <html>
      <head></head>
      <body>
        <p>Hi All!<br><br>
        Not Analysis Test Cases to be completed, please take actions!!<br>
        Time: """ + date + """
            <table border="1" class="t1">
              <tr>
                <th>Name</th> """ + headers + """
              </tr>""" + output_bodies + """
            </table>
        </p>
      </body>
    </html>
    """
    return html_temp