// on click of a tag, it should be toggled - either added to or removed from an internal tracking
// array and its style changed.
//
// When the internal array changes, it should write out a new tag list to the hidden input

document.addEventListener("DOMContentLoaded", () => {
    var elems = document.getElementsByClassName("taggit-labels")
    for (var i = 0; i < elems.length; i++) {
        let e1 = elems[i].closest("div")
        let inputs = e1.querySelectorAll(".taggit-labels + input")[0];
        let tagItems = e1.querySelectorAll(".taggit-list .taggit-tag");
        tagItems.forEach(function(t) {
            t.addEventListener('click', function() {
                let tagList = inputs.value ? inputs.value.split(", ") : []
                let tagName = this.getAttribute("data-tag-name");
                if(tagName.indexOf(",") != -1 || tagName.indexOf(" ") != -1) {
                    tagName = "\"" + tagName + "\"";
                }
                let index = tagList.indexOf(tagName);
                if(index == -1) {
                    this.classList.toggle("selected");
                    tagList.push(tagName);
                } else {
                    this.classList.toggle("selected");
                    tagList.splice(index, 1);
                }
                inputs.setAttribute("value", tagList.join(", "));
            });
        });
    }
});
