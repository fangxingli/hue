
<%!
def is_selected(section, matcher):
  if section == matcher:
    return "active"
  else:
    return ""
%>

<%def name="menubar(section='')">
  <div class="navbar navbar-inverse navbar-fixed-top nokids">
    <div class="navbar-inner">
      <div class="container-fluid">
        <div class="nav-collapse">
          <ul class="nav">
            <li class="currentApp">
              <a href="/boc">
                <img src="${ static('boc/art/icon_boc_48.png') }" class="app-icon" />
                Boc
              </a>
             </li>
             <li class="${is_selected(section, 'query')}"><a href="/boc">查询场景</a></li>
             <li class="${is_selected(section, 'management')}"><a href="/boc/admin">管理查询场景</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
