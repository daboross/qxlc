function submitLink() {
    var $linkArea = $("#link-area");
    var original_url = $linkArea.val();
    $linkArea.val("");

    var $resultRow = $('<tr/>');
    var $resultLeft = $('<p/>').text(truncateData(original_url));
    var $resultRight = $('<p>').text('Submitting...');
    $resultRow.append($('<td/>').append($resultLeft));
    $resultRow.append($('<td/>').append($resultRight));
    $('#results-table').prepend($resultRow);

    var $request = $.ajax(
        {
            url: "/api/shorten",
            type: "POST",
            data: {"url": original_url},
            dataType: "text"
        }
    );
    $request.success(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $resultInner = $("<input/>").attr("type", "text").attr("class", "form-control").val(data);
        var $newResult = $("<p/>").append($resultInner);
        $resultRight.replaceWith($newResult);
        $resultInner.click(function () {
            select($resultInner);
        });
        select($resultInner);
    });
    $request.fail(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $newResult = $("<p/>").text("Failed: " + data.responseText);
        $resultRight.replaceWith($newResult);
    });
}

function submitPaste() {
    var $pastArea = $("#paste-area");
    var data = $pastArea.val();
    $pastArea.val("");

    var $resultRow = $('<tr/>');
    var $resultLeft = $('<p/>').text(truncateData(data));
    var $resultRight = $('<p>').text('Submitting...');
    $resultRow.append($('<td/>').append($resultLeft));
    $resultRow.append($('<td/>').append($resultRight));
    $('#results-table').prepend($resultRow);

    var $request = $.ajax(
        {
            url: "/api/paste",
            type: "POST",
            data: {"paste": data},
            dataType: "text"
        }
    );
    $request.success(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $resultInner = $("<input/>").attr("type", "text").attr("class", "form-control").val(data);
        var $newResult = $("<p/>").append($resultInner);
        $resultRight.replaceWith($newResult);
        $resultInner.click(function () {
            select($resultInner);
        });
        select($resultInner);
    });
    $request.fail(function (data, textStatus, jqXHR) {
        $('#results-div').show();
        var $newResult = $("<p/>").text("Failed: " + data.responseText);
        $resultRight.replaceWith($newResult);
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
function select(element) {
    element.focus();
    element.select();
}

$(document).ready(function () {
    $('#link-area').keydown(function (event) {
        if (event.keyCode == 13) {
            submitLink();
            return false;
        }
        return true;
    });
    $("#link-submit").click(submitLink);
    $("#paste-submit").click(submitPaste)
});
