from src.core.prompts_templetes.rules import (
    PRICE_PROMPT,
    AVAILABILITY_PROMPT,
    SPECS_PROMPT,
    COMPARE_PROMPT,
    SEARCH_PROMPT,
    SHIPPING_PROMPT,
    WARRANTY_PROMPT,
    RETURN_PROMPT,
    GENERAL_PROMPT,
)


PROMPT_MAP = {
    "ask_price": PRICE_PROMPT,
    "product_availability": AVAILABILITY_PROMPT,
    "product_specifications": SPECS_PROMPT,
    "compare_products": COMPARE_PROMPT,
    "search_product": SEARCH_PROMPT,
    "ask_shipping": SHIPPING_PROMPT,
    "ask_warranty": WARRANTY_PROMPT,
    "ask_return": RETURN_PROMPT,
    "ask_about_order": GENERAL_PROMPT,
    "others": GENERAL_PROMPT,
}

_BASE_SYSTEM_PROMPT = (
    "أنت مساعد ذكي متخصص في الإجابة على الأسئلة باللغة العربية الفصحى.\n\n"
    "🔒 قواعد صارمة يجب الالتزام بها:\n"
    "1. استخدم فقط المعلومات الموجودة حرفيًا في 'السياق'.\n"
    "2. ممنوع تمامًا استخدام أي معرفة خارجية أو تخمين أو استنتاج غير مذكور صراحة.\n"
    "3. لا تضف أي ميزة أو مواصفة غير موجودة في السياق.\n"
    "4. إذا لم تجد المعلومة في السياق، اكتب فقط:\n"
    "   'لا تتوفر لديّ معلومات كافية للإجابة على هذا السؤال.'\n"
    "5. عند المقارنة: اعرض المعلومات كما هي في السياق لكل عنصر.\n"
    "6. لا تفترض معلومات ضمنية إلا إذا كانت مذكورة.\n"
    "7. اجعل الإجابة قصيرة، دقيقة، ومباشرة.\n"
)


def build_prompt(intent: str, question: str, context: str) -> list[dict]:
    """
    Builds the chat-template messages list (system + user) for the LLM.
    Returns list[dict] as required by HuggingFace apply_chat_template().
    """
    intent_rules = PROMPT_MAP.get(intent, GENERAL_PROMPT)
    system_prompt = _BASE_SYSTEM_PROMPT + "\n" + intent_rules

    user_content = (
        "اقرأ السياق بعناية ثم أجب.\n\n"
        f"### السياق:\n{context}\n\n"
        f"### السؤال:\n{question}\n\n"
        "⚠️ تذكير: لا تخرج عن السياق تحت أي ظرف."
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]