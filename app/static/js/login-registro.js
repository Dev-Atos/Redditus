 $("#username, #rcpf_cnpj").keydown(function(){
    try {
        $("#username, #rcpf_cnpj").unmask();
    } catch (e) {}

    var tamanho = $("#username, #rcpf_cnpj").val().length;

    if(tamanho < 11){
        $("#username, #rcpf_cnpj").mask("999.999.999-99");
    } else {
        $("#username, #rcpf_cnpj").mask("99.999.999/9999-99");
    }

    // ajustando foco
    var elem = this;
    setTimeout(function(){
        // mudo a posição do seletor
        elem.selectionStart = elem.selectionEnd = 10000;
    }, 0);
    // reaplico o valor para mudar o foco
    var currentValue = $(this).val();
    $(this).val('');
    $(this).val(currentValue);
});