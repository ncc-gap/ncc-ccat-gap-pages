var appendTOC = !function() {
    // 設定
    var correctTarget = '#contents';
    var correctTargetHeadings = 'h2, h3';

    //#toc要素が存在する場合のみ動作
    if ($('#toc').length <= 0) {
        return false;
    }

    //見出しを収集
    var $h = $(correctTarget).find(correctTargetHeadings);

    // 目次を作成
    var html = '<ul class="toc-list">';
    $h.each(function(i, v) {
    	var c = 'toc-' + $(v).context.nodeName.toLowerCase();
        html += '<li class="' + c + '"><a data-toc="' + i + '">';
        html += $(v).text();
        html += '</a></li>';
    });
    html += '</ul>';

    $('#toc').html(html);

    //目次クリック時のスクロールイベント
    $(document).on('click', '#toc .toc-list a', function() {
        var no = +$(this).attr('data-toc');
        var target = $(correctTarget).find(correctTargetHeadings)[no];
        var targetPosition = $(target).offset().top;
        $('body,html').animate({
            scrollTop: targetPosition
        }, 500, 'swing');
        return false;
    });
}();