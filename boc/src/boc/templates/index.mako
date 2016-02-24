<%!from desktop.views import commonheader, commonfooter %>
<%namespace name="shared" file="shared_components.mako" />

${commonheader("Boc", "boc", user) | n,unicode}
${shared.menubar(section='mytab')}

## Use double hashes for a mako template comment
## Main body

<iframe style="width: 100%; height:900px;" frameBorder=0 src='/boc/query'></iframe>

${commonfooter(request, messages) | n,unicode}
