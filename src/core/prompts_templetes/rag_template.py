from src.core.prompts_templetes.rules import (
    PRICE_PROMPT, 
    AVAILABILITY_PROMPT, 
    SPECS_PROMPT, 
    COMPARE_PROMPT, 
    SEARCH_PROMPT, 
    SHIPPING_PROMPT, 
    WARRANTY_PROMPT, 
    RETURN_PROMPT, 
    GENERAL_PROMPT
)

PROMPT_MAP = {
    'ask_price': PRICE_PROMPT, 
    'product_availability': AVAILABILITY_PROMPT, 
    'product_specifications': SPECS_PROMPT, 
    'compare_products': COMPARE_PROMPT, 
    'search_product': SEARCH_PROMPT, 
    'ask_shipping': SHIPPING_PROMPT, 
    'ask_warranty': WARRANTY_PROMPT, 
    'ask_return': RETURN_PROMPT, 
    'ask_about_order': GENERAL_PROMPT, 
    'others': GENERAL_PROMPT
}
_BASE_SYSTEM_PROMPT = "أنت مساعد ذكي ومندوب مبيعات متخصص في الإجابة على الأسئلة باللغة العربية الفصحى.\n\n   قواعد صارمة يجب الالتزام بها:\n. استخدم فقط المعلومات المستخرجة من 'السياق'.\n. ممنوع تمامًا استخدام أي معرفة خارجية أو تخمين.\n. لا تضف أي ميزة أو مواصفة غير موجودة في السياق.\n. إذا لم تجد المعلومة في السياق أبداً، اكتب فقط:\n   'لا تتوفر لديّ معلومات كافية للإجابة على هذا السؤال.'\n. عند إعطاء السعر، اكتب السعر بوضوح حتى لو كان 0.0.\n. اجعل الإجابة قصيرة، دقيقة، ومباشرة.\n"

def build_prompt(intent: str, question: str, context: str) -> list[dict]:
    intent_rules = PROMPT_MAP.get(intent, GENERAL_PROMPT)
    system_prompt = _BASE_SYSTEM_PROMPT + '\n' + intent_rules
    user_content = f'اقرأ السياق بعناية ثم أجب.\n\n### السياق:\n{context}\n\n### السؤال:\n{question}\n\n تذكير: لا تخرج عن السياق تحت أي ظرف.'
    return [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_content}]