
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
              <a href="/user_profile">
                <img src="${ static('user_profile/art/icon_user_profile_48.png') }" class="app-icon" />
                用户画像
              </a>
             </li>
             <li class="${is_selected(section, 'tag_search')}"><a href="tag_search">标签甄选系统</a></li>
             <li class="${is_selected(section, 'tag_heat')}"><a href="tag_heat">理财产品分析</a></li>
             <li class="${is_selected(section, 'relationship')}"><a href="relationship">人群关系图谱</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>
