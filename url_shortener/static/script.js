window.onload = function() {
    var body = document.getElementsByTagName('body')[0]

    body.addEventListener('click', function(e) {
        if (e.target.id === 'copy-button') {
            var selection = window.getSelection();
	        var range = document.createRange();

	        var newUrlNode = document.getElementById('new-url');

	        range.selectNodeContents(newUrlNode);
	        selection.removeAllRanges();
	        selection.addRange(range);
	        document.execCommand('copy');
	        selection.removeAllRanges();
        }
    });
}