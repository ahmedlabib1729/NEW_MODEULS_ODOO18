odoo.define('website_saleorder_create.search', function (require) {
    'use strict';

    var ajax = require('web.ajax');  // استدعاء مكتبة AJAX
    var $ = require('jquery');

    $(document).ready(function () {
        $('#search-button').on('click', function () {
            var searchQuery = $('#search-query').val();
            var categoryId = $('#category-filter').val();

            // إرسال طلب AJAX إلى '/order/search'
            ajax.jsonRpc('/order/search', 'call', {
                search_query: searchQuery,
                category_id: categoryId
            }).then(function (data) {
                // تحديث الجدول بالمنتجات المسترجعة
                var productList = $('#product-list');
                productList.empty();

                if (data.products && data.products.length > 0) {
                    data.products.forEach(function (product) {
                        productList.append(`
                            <tr>
                                <td class="text-center">
                                    <input type="checkbox" name="product_id" value="${product.id}" class="form-check-input"/>
                                </td>
                                <td>${product.name}</td>
                                <td>${product.price}</td>
                            </tr>
                        `);
                    });
                } else {
                    productList.append('<tr><td colspan="3" class="text-center">لا توجد منتجات مطابقة.</td></tr>');
                }
            }).fail(function () {
                alert('حدث خطأ أثناء البحث. الرجاء المحاولة مرة أخرى.');
            });
        });
    });
});
