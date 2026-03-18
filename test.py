from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# ── Device ───────────────────────────────────────────────────────────────────
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# ── Model paths ───────────────────────────────────────────────────────────────
LOCAL_MODEL_PATH = r"src\core\models\Qwen2.5-1.5B-Instruct"
HF_MODEL_ID      = "Qwen/Qwen2.5-1.5B-Instruct"

# ── Load tokenizer & model ────────────────────────────────────────────────────
print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_PATH)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    LOCAL_MODEL_PATH,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
    device_map=device,
)
model.eval()

# ── Prompt builder ────────────────────────────────────────────────────────────
def qwen_rag_template(question: str, context: str, history: list[dict]) -> list[dict]:
    system_prompt = (
        "أنت مساعد ذكي متخصص في الإجابة على الأسئلة باللغة العربية الفصحى.\n\n"
        
        "🔒 قواعد صارمة يجب الالتزام بها:\n"
        "1. استخدم فقط المعلومات الموجودة حرفيًا في 'السياق'.\n"
        "2. ممنوع تمامًا استخدام أي معرفة خارجية أو تخمين أو استنتاج غير مذكور صراحة.\n"
        "3. لا تضف أي ميزة أو مواصفة غير موجودة في السياق.\n"
        "4. إذا لم تجد المعلومة في السياق، اكتب فقط:\n"
        "   'لا تتوفر لديّ معلومات كافية للإجابة على هذا السؤال.'\n"
        "5. عند المقارنة:\n"
        "   - اعرض المعلومات كما هي في السياق لكل عنصر.\n"
        "   - لا تستنتج الأفضلية إلا إذا كانت مبنية مباشرة على الأرقام المذكورة.\n"
        "6. لا تفترض معلومات ضمنية (مثل جودة الشاشة أو الكاميرا) إلا إذا كانت مذكورة.\n"
        "7. يجب أن تكون كل جملة في الإجابة قابلة للإرجاع إلى السياق.\n"
        "8. إذا وجدت تعارضًا أو نقصًا في البيانات، وضّح ذلك بدلاً من التخمين.\n"
        "9. اجعل الإجابة قصيرة، دقيقة، ومباشرة.\n"
        "10. لا تقم بتحديد أي منتج \"أفضل\" إلا إذا كان ذلك مذكورًا صراحة في السياق.\n"
        "11. لا تفترض أن رقم المعالج الأعلى يعني أداء أفضل، فقط اعرض البيانات كما هي.\n"
        "12. عند المقارنة، لا تستخدم كلمات مثل (أفضل، أقوى، أسرع) إلا إذا كانت مدعومة مباشرة من النص.\n"
    )

    user_content = (
        "اقرأ السياق بعناية ثم أجب.\n\n"
        f"### السياق:\n{context}\n\n"
        f"### السؤال:\n{question}\n\n"
        "⚠️ تذكير: لا تخرج عن السياق تحت أي ظرف."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_content})

    return messages

# ── Inference function ────────────────────────────────────────────────────────
def generate(messages: list[dict], max_new_tokens: int = 256) -> str:
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)


# ── RAG pipeline entry point ──────────────────────────────────────────────────
def rag_answer(question: str, context: str, history: list[dict] = []) -> str:
    messages = qwen_rag_template(question, context, history)
    return generate(messages)


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    context  = """
productName: لابتوب ديل انسبايرون brand: Dell category: لابتوبات price: 25000.00  availability: متاح  stock: 5 وحدة  description: لابتوب بمعالج Intel Core i7 الجيل الثالث عشر، ذاكرة 16 جيجا، SSD 512 جيجا
productName: لابتوب لينوفو ثينكباد  brand: Lenovo category: لابتوبات price: 30000.00 availability: متاح stock: 3 وحدة  description: لابتوب بمعالج Intel Core i9، ذاكرة 32 جيجا، SSD 1 تيرا، مناسب للأعمال
productName: ايفون 15 برو brand: Apple category: موبايلات price: 45000.00 availability: متاح stock: 10 وحدة  description: شاشة 6.1 بوصة Super Retina، معالج A17 Pro، كاميرا 48 ميجابكسل
"""
    history = []

    print("💬 نظام RAG جاهز. اكتب 'exit' للخروج.\n")

    while True:
        question = input("👤 سؤالك: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("👋 تم إنهاء الجلسة.")
            break

        answer = rag_answer(question, context, history)

        print("🤖:", answer, "\n")

        # تحديث الـ history (مهم للـ multi-turn)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})