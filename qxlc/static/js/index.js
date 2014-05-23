function submitLink() {
    var $linkArea = $("#link-area");
    var original_url = $linkArea.val();
    $linkArea.val("");

    var $result = $('<div/>').text('Submitting...');
    $("#link-result").prepend($result);

    var $request = $.ajax({
                              url: "/api/shorten?" + $.param({"url": original_url, "api_key": ""}),
                              type: "GET",
                              dataType: "text"
                          });
    $request.success(function (data, textStatus, jqXHR) {
        var inner_html = $("<a/>").attr("href", data).text("[" + original_url + "] " + data);
        var new_html = $("<p/>").append(inner_html);
        $result.replaceWith(new_html)
    });
    $request.fail(function (data, textStatus, jqXHR) {
        var new_html = $("<p/>").text("[" + original_url + "] Failed: " + data.responseText);
        $result.replaceWith(new_html)
    });
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
