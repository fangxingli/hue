<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("User Profile", "user_profile", user, padding="70px") | n,unicode}
${shared.menubar(section='tag_search')}

## Use double hashes for a mako template comment
## Main body

## <div class="container-fluid">
##   <div class="card">
##     <h2 class="card-heading simple">User Profile app is successfully setup!</h2>
##     <div class="card-body">
##       <p>It's now ${date}.</p>
##     </div>
##   </div>
## </div>

<iframe style="width: 100%; height:900px;" frameBorder=0 src='index'></iframe>
${commonfooter(request, messages) | n,unicode}
