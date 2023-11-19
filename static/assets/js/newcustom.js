document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.FontTapUpper').addEventListener('click', function() {
        document.querySelector('.FontsBoxxxTap').classList.add('showTap');
    });

    document.querySelector('.dlg-close-btn').addEventListener('click', function() {
        document.querySelector('.FontsBoxxxTap').classList.remove('showTap');
    });

    document.querySelectorAll('.category').forEach(function(element) {
        element.addEventListener('click', function() {
            document.querySelector('.content_Font').classList.add('show-category');
            document.querySelector('.browse-categories').classList.add('show-Item');
            
            var categoryText = this.textContent;
            document.querySelector('.dlg-header-title span').textContent = categoryText;
        });
    });

    document.querySelector('.browse-categories').addEventListener('click', function() {
        this.classList.remove('show-Item');
        document.querySelector('.content_Font').classList.remove('show-category');
        document.querySelector('.dlg-header-title span').textContent = 'Choose a Category Font';
    });

    document.querySelectorAll('.font').forEach(function(element) {
        element.addEventListener('click', function() {
            document.querySelectorAll('.font').forEach(function(fontElement) {
                fontElement.classList.remove('selected');
            });

            this.classList.add('selected');
            
            var fontName = this.querySelector('.name').textContent;
            document.querySelector('.FontTapUpper .namoffont').textContent = fontName;
            changeFontFamily(fontName);
        });
    });
});