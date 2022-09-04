function new_item(type_class="", content="") {
    var item = document.createElement("div");
    item.classList.add("md-block");
    if (type_class.length != 0) {
        console.log(type_class);
        item.classList.add(type_class);
    }
    if (content.length == 0) {
        item.appendChild(document.createElement("br"));
    } else {
        item.appendChild(document.createTextNode(content));
    }
    return item;
};

function parse_line(content) {
    var ws_pos = content.indexOf(" ");
    var tag;
    if (ws_pos == -1) {
        return ["", content];
    }
    var possible_tag = content.slice(0, ws_pos);
    if (possible_tag == "#") {
        tag = "h1";
    } else if (possible_tag == "##") {
        tag = "h2";
    } else {
        return ["", content];
    }
    return [tag, content.slice(ws_pos + 1)];
}

function set_cursor_at(selection, anchor_node, offset=0) {
    selection.setBaseAndExtent(anchor_node, offset, anchor_node, offset);
}

function tag2class(tag) {
    if (tag == "#") {
        return "md-h1";
    }
    if (tag == "##") {
        return "md-h2";
    }
    if (tag == ">") {
        return "md-quote";
    }
    if (tag == "-") {
        return "md-list";
    }
    if (tag == "--") {
        return "md-sublist";
    }
    if (tag == "[]") {
        return "md-check";
    }
    return "";
}

$(".md-editor").each(function(){
    // 暂时不考虑有其他 element 如 <b><u>  等的情形
    $( this ).attr("contenteditable", "true");
    $( this ).on('keydown', function(e) {
        // backspace
        var selection = getSelection();
        var cursor_node = selection.anchorNode;
        var start_offset = selection.anchorOffset;
        var md_block;
        if (e.keyCode == 8) {
            if (cursor_node instanceof Text) {
                return true;
            }
            if (!selection.isCollapsed) {
                // 有一个问题是第一行的格式没法被删除
                return true;
            }
            console.log(cursor_node);
            // 如果没有 text 可选，说明是 md-block 且是空行
            if (!cursor_node instanceof Element || !cursor_node.classList.contains("md-block")) {
                var tag_name = cursor_node.tagName.toLowerCase();
                if (tag_name == "br" || tag_name == "b") {
                    md_block = cursor_node.closest(".md-block");
                    if (md_block == md_block.parentElement.firstElementChild) {
                        md_block.removeChild(cursor_node);
                        md_block.appendChild(document.createElement("br"));
                        md_block.classList = ["md-block"];
                    }
                    console.log("should be empty <b>")
                    return true;
                }
                alert("error!");
                console.log("cursor node:", cursor_node, tag_name);
                return false;
            }
            // 有格式，这个判断方法有待改进
            if (cursor_node.classList.length > 1) {
                cursor_node.classList = ["md-block"];
                return false;
            }
            // 第一行
            if (cursor_node == cursor_node.parentElement.firstElementChild) {
                return false;
            }
            return true;
        }

        // whitespace
        // possible format:
        //  1. #
        //  2. >
        //  3. - 
        else if (e.keyCode == 32) {
            if (!(cursor_node instanceof Text)) {
                console.log("Not text!");
                return true;
            }
            var md_class = tag2class(cursor_node.data.slice(0, selection.anchorOffset));
            if (md_class) {
                md_block = cursor_node.parentElement;
                if (!md_block.classList.contains("md-block")) {
                    console.log(md_block, md_block.parentElement);
                    md_block = md_block.closest(".md-block");
                }
                // cursor_node.parentElement.closest("md-block").classList.add(md_class);
                md_block.classList.add(md_class);
                cursor_node.data = cursor_node.data.slice(selection.anchorOffset);
                if (!cursor_node.data) {
                    cursor_node.parentElement.appendChild(document.createElement("br"));
                }
                return false;
            }
        }

        // else if (e.keyCode == 13) {
        //     console.log(cursor_node.nextSibling);
        //     if (cursor_node instanceof Text && cursor_node.nextSibling == null) {
        //         // 问题是会复制上一行的格式，如果是引用，list 还好，但如果是标题最好不复制格式
        //         // 再说吧，短期内问题不大
        //         // if (cursor_node.parentElement.classList.contains("md-h1") || 
        //         //     cursor_node.parentElement.classList.contains("md-h2")) {
        //         //     return false;
        //         // }
        //         return true;
        //     }
        // }
        else if (e.ctrlKey && e.key == "s") {
            console.log("Gotcha");
        }
        return true;
    });
});
