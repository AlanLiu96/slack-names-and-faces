// https://app.slack.com/client/[workspace_id]/browse-people

 imageList = []
 nameList = []
 titleList =[]

// rerun on different pages
grid = document.getElementsByClassName('p-bp__grid_cell')
for (let item of grid) {
    imageList.push(item.getElementsByClassName('c-base_icon')[0]["src"])
    nameList.push(item.getElementsByClassName('p-browse_page_member_card_entity__name_text')[0].children[0].innerText)
    let title = item.getElementsByClassName('p-browse_page_member_card_entity__subtext')[0].children[0]
    if (typeof title !== 'undefined') {
        titleList.push(title.innerText)
    } else {
        titleList.push('Unknown')
    }
}


// Run from channel member list
 realNameList = []
 nameList = []
 imageList = []

grid = document.getElementsByClassName('c-virtual_list__scroll_container')[2].children
for (let item of grid){
    if (item.id === 'anchor_hack_item' || item.id === 'add_member'){
        continue;
    }

    imageList.push(item.getElementsByClassName('c-avatar')[0].children[0].src)

    let pref_name_text = item.getElementsByClassName('c-member_name')[0].children[0].innerText
    nameList.push(pref_name_text)

    let real_name = item.getElementsByClassName('c-member__secondary-name')[0]
    if (typeof real_name !== 'undefined'){
        realNameList.push(real_name.children[0].innerText)
    } else {
        realNameList.push(pref_name_text)
    }
}
