import json
from typing import Dict, Any
from datetime import datetime
from pathlib import Path

def format_output(metrics: Dict[str, Any], format_type: str = "cli", output_file: str = None) -> str:
    """
    Formata a saída das métricas no formato especificado.
    
    Args:
        metrics: Dicionário com as métricas coletadas
        format_type: Tipo de formato ('cli', 'json')
        output_file: Caminho do arquivo de saída (opcional)
    
    Returns:
        str: Mensagem de confirmação ou dados formatados
    """
    if format_type.lower() == "json":
        output = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        
        if output_file:
            # Garante que o diretório existe
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            return f"✅ Resultados salvos em: {output_file}"
        else:
            return json.dumps(output, indent=4, ensure_ascii=False)
    
    return None 