// Função utilitária para limpar valores estatísticos com problemas
function cleanStatValue(value) {
    if (!value) return '0';
    
    // Conversão para string
    let textValue = String(value);
    
    // Verificar problemas comuns
    if (textValue.includes('...') || textValue.endsWith('..') || 
        textValue.includes('..') || textValue.match(/^\d+\.\./) || 
        textValue.includes('[') || textValue.includes(']')) {
        
        // Remover parênteses, colchetes e seu conteúdo
        textValue = textValue.replace(/\[\d+\]/g, '').replace(/\(\d+\)/g, '');
        
        // Remover pontos extras
        textValue = textValue.replace(/\.\.+/g, '').replace(/\.$/g, '');
        
        // Extrair apenas números
        const numMatch = textValue.match(/^(\d+)/);
        if (numMatch) {
            textValue = numMatch[1];
        }
        
        // Se ficar vazio após limpeza, usar '0'
        if (textValue.trim() === '') {
            return '0';
        }
    }
    
    return textValue.trim();
}
