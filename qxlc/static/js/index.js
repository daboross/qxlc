var valid_url = /^(?:(?:http|ftp)s?:\/\/)?(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:\/ ?|[\/?]\S+)$/;

function submitContent() {
    var $contentArea = $("#content-area");
    var data = $contentArea.val();
    $contentArea.val("");

    var $resultRow = $('<tr/>');
    var $column1 = $('<p/>');
    var $column2 = $('<p/>').text(truncateData(data));
    var $column3 = $('<p/>').text('Submitting...');
    if (valid_url.test(data)) {
        $column1.text("Url");
    } else {
        $column1.text("Paste");
    }
    $resultRow.append($('<td/>').append($column1));
    $resultRow.append($('<td/>').append($column2));
    $resultRow.append($('<td/>').append($column3));
    $('#results-table').prepend($resultRow);

    var $request = $.ajax(
        {
            url: "/api/generic-submit",
            type: "POST",
            data: {"content": data},
            dataType: "text"
        }
    );
    $request.success(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $resultInner = $("<input/>").attr("type", "text").attr("class", "form-control").val(data);
        var $newResult = $("<p/>").append($resultInner);
        $column3.replaceWith($newResult);
        $resultInner.click(function () {
            selectAll($resultInner);
        });
        selectAll($resultInner);
    });
    $request.fail(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $newResult = $("<p/>").text("Failed: " + data.responseText);
        $column3.replaceWith($newResult);
    });
}

function truncateData(long_data) {
    var data = long_data;
    if (data.indexOf("\n") > -1) {
        data = data.split("\n")[0];
    }
    data = data.substring(0, Math.min(data.length, 10));
    if (data !== long_data) {
        data += "..."
    }
    return data
}
function selectAll(element) {
    element.focus();
    element.select();
}
function cursorSelect(element) {
    element.focus();
    element.setSelectionRange(0, 0);
}

$(document).ready(function () {
    var contentArea = $('#content-area');
    var contentSubmit = $('#content-submit');

//    contentArea.keydown(function (event) {
//        if (event.keyCode == 13) { // enter
//            submitContent();
//            return false;
//        }
//        return true;
//    });
    contentArea.keydown(function (event) {
        if (event.ctrlKey && event.keyCode == 83) { // ctrl+s
            submitContent();
            return false;
        }
        return true;
    });

    contentSubmit.click(submitContent);

    cursorSelect(contentArea);
});
