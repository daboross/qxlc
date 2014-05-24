function submitLink() {
    var $linkArea = $("#link-area");
    var original_url = $linkArea.val();
    $linkArea.val("");

    var $resultRow = $('<tr/>');
    var $resultLeft = $('<p/>').text(original_url);
    var $resultRight = $('<p>').text('Submitting...');
    $resultRow.append($('<td/>').append($resultLeft));
    $resultRow.append($('<td/>').append($resultRight));
    $('#link-result').prepend($resultRow);

    var $request = $.ajax({
                              url: "/api/shorten?" + $.param({"url": original_url, "api_key": ""}),
                              type: "GET",
                              dataType: "text"
                          });
    $request.success(function (data, textStatus, jqXHR) {
        $('#link-result-group-item').show()
        var $inner_html = $("<input/>").attr("type", "text").attr("class", "form-control").val(data);
        var $new_html = $("<p/>").append($inner_html);
        $resultRight.replaceWith($new_html);
        $inner_html.click(function () {
            select($inner_html);
        });
    });
    $request.fail(function (data, textStatus, jqXHR) {
        $('#link-result-group-item').show()
        var new_html = $("<p/>").text("Failed: " + data.responseText);
        $resultRight.replaceWith(new_html);
    });
}
function select(element) {
    console.log("Selecting " + element);
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
    $("#link-submit-button").click(submitLink);
});
