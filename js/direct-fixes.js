/**
 * Correções diretas para problemas específicos
 */

(function() {
    console.log('Aplicando correções diretas...');
    
    // Função para corrigir valores com "..."
    function fixDottedValues(value) {
        if (!value) return '0';
        
        let strValue = String(value);
        // Corrigir valores como "1..." ou "1.."
        if (strValue.includes('...') || strValue.endsWith('..') || strValue.match(/^\d+\.\./) || strValue === '1..') {
            const numMatch = strValue.match(/^(\d+)/);
            return numMatch ? numMatch[1] : '0';
        }
        
        return strValue;
    }
    
    // Função para corrigir nacionalidades com [xx]
    function fixNationality(nationality) {
        if (!nationality) return nationality;
        return nationality.replace(/\s*\[\d+\]\s*/g, '');
    }
    
    // Função principal para aplicar correções
    function applyFixes() {
        // 1. Modificar diretamente os elementos DOM exibidos
        
        // Corrigir pole positions com "..."
        document.querySelectorAll('.pole-positions-value').forEach(el => {
            const originalValue = el.textContent;
            if (originalValue.includes('...') || originalValue.endsWith('..')) {
                el.textContent = fixDottedValues(originalValue);
                console.log(`Corrigido pole positions: ${originalValue} → ${el.textContent}`);
            }
        });
        
        // Corrigir outros valores estatísticos
        const statClasses = [
            '.championships-value',
            '.race-entries-value',
            '.race-starts-value',
            '.wins-value',
            '.podiums-value',
            '.fastest-laps-value'
        ];
        
        statClasses.forEach(className => {
            document.querySelectorAll(className).forEach(el => {
                const originalValue = el.textContent;
                if (originalValue.includes('...') || originalValue.endsWith('..')) {
                    el.textContent = fixDottedValues(originalValue);
                    console.log(`Corrigido ${className}: ${originalValue} → ${el.textContent}`);
                }
            });
        });
        
        // 2. Garantir que temporadas estejam na mesma linha com espaçamento correto
        document.querySelectorAll('.seasons-stat').forEach(statEl => {
            // Garantir centralização e nowrap
            statEl.style.textAlign = 'center';
            statEl.style.whiteSpace = 'nowrap';
            
            // Verificar se o piloto tem temporadas longas
            const seasonValue = statEl.querySelector('.seasons-value');
            if (seasonValue && seasonValue.textContent.length > 15) {
                // Aplicar estilo adaptativo para temporadas longas
                seasonValue.style.fontSize = '0.8rem';
                seasonValue.style.letterSpacing = '-0.5px';
            }
            
            // Garantir espaçamento correto
            const labelEl = statEl.querySelector('.label');
            if (labelEl) {
                labelEl.style.marginRight = '0.2rem';
            }
        });
        
        console.log('Correções diretas aplicadas com sucesso!');
    }
    
    // Executar quando o DOM estiver totalmente carregado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyFixes);
    } else {
        // DOM já está carregado
        applyFixes();
    }
    
    // Tentar novamente após um segundo para garantir
    setTimeout(applyFixes, 1000);
    
    // E mais uma vez após o carregamento completo
    window.addEventListener('load', () => {
        setTimeout(applyFixes, 500);
    });
})();
