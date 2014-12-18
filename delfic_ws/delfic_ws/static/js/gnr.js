var GNR = {};
GNR.Ui = {};

$(document).ready(function () {
    GNR.init();
});

GNR.init = function () {
    GNR.components = {};
    GNR.components.loader = GNR.Ui.CompanyLoader('#company-details');
}

GNR.Ui.CompanyLoader = function (container) {

    var _loader = {};
    var _container = $(container);

    function init() {
        $('#process-companies').click(function (e) {
            e.preventDefault();
            var items = $('.company-item');
            var linkArr = [];
            items.each(function (i) {
                var a = $('.company-link', this);
                var link = a.attr('href');
                var resultDiv = $('.url-result', this);
                var comp = a.text();
                linkArr.push({link: link, comp: comp, resultDiv: resultDiv});
                //_loader.ProcessCompany(companyRef);
            });
            getLink(linkArr, 0);
        });

        $('#filter-companies').click(function (e) {
            e.preventDefault();

            var items = $('.company-item');
            var remItems = [];
            items.each(function (i) {
                var a = $('.url-result a', this);
                if (!a.length) {
                    remItems.push(items[i]);
                }
            });
            for (var i = 0; i < remItems.length; i++) {
                var item = remItems[i];
                item.remove();
            }
            $('#process-company-websites').removeClass('hidden');
        });

        $('#process-company-websites').click(function (e) {
            e.preventDefault();
            var items = $('.company-item');
            var linkArr = [];
            items.each(function (i) {
                var a = $('.url-result a', this);
                if (a.length) {
                    var link = a.attr('href');
                    var resultUl = $('.stats ul', this);
                    linkArr.push({link: link, resultUl: resultUl});
                }
            });
            getCompanyLinks(linkArr, 0);
        });
        initAjax();
    }

    function getLink(linkArr, curIndex) {
        $.ajax(
            {
                type: "POST",
                url: linkArr[curIndex].link,
                success: linkSuccess,
                dataType: 'json',
                error: linkError,
                complete: linkComplete
            }
        );
        function linkSuccess(data) {
            _container.removeClass('hidden');
            var result = '';
            if (data.success) {
                result = '<a href="' + data.url + '" target="_blank">' + data.url + '</a>';
            } else {
                result = data.message;
            }
            linkArr[curIndex].resultDiv.html(result);

        }

        function linkError(x, s, e) {
            if (e) {
                linkArr[curIndex].resultDiv.html(e);
            } else {
                linkArr[curIndex].resultDiv.html('ajax error');
            }
        }

        function linkComplete() {
            if (curIndex < linkArr.length - 1) {
                getLink(linkArr, curIndex + 1);
            } else {
                $('#filter-companies').removeClass('hidden');
            }
        }
    }


    function getCompanyLinks(linkArr, curIndex) {
        $.ajax(
            {
                type: "POST",
                url: "http://127.0.0.1:8000/findcompanylinks/",
                data: {"url": linkArr[curIndex].link},
                success: linkSuccess,
                dataType: 'json',
                error: linkError,
                complete: linkComplete
            }
        );
        function linkSuccess(data) {
            linkArr[curIndex].resultUl.append('<li><br></li>')
            if (data.success) {
                for (var i = 0; i < data.links.length; i++) {
                    var link = data.links[i];
                    var li = $('<li><span class="stat-label">' + link.title + ':</span><span class="top-link">' + link.link + '</span></li>');
                    linkArr[curIndex].resultUl.append(li);
                }
            } else {
                linkArr[curIndex].resultUl.append('<li><span class="stat-label">Top Link Error:</span><span class="top-link">' + data.message + '</span></li>');
            }

        }

        function linkError(x, s, e) {
            if (e) {
                linkArr[curIndex].resultUl.append('<li>' + e + '</li>')
            } else {
                linkArr[curIndex].resultUl.append('<li>' + 'ajax error' + '</li>');
            }
        }

        function linkComplete() {
            if (curIndex < linkArr.length - 1) {
                getCompanyLinks(linkArr, curIndex + 1);
            } else {
                $('#filter-companies').removeClass('hidden');
            }
        }
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function initAjax() {
        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    _loader.ProcessCompany = function (data) {
        _container.removeClass('hidden');
        $('.process-status', _container).html(data)
    };

    init();
    return _loader;

};