# Ted Med

## Inspiration

Hospitals can be overwhelming and even terrifying for children-- and for **93% of children it is**. The sterile environment, unfamiliar faces, and intimidating medical procedures often make kids too scared, shy, or nervous to express what they’re feeling. This lack of communication leads to missed symptoms, delayed diagnoses, and inaccurate health records—problems that can directly impact a child’s health and well-being.

I saw the severity of this issue firsthand through my brother, who worked as a patient care assistant for five years at the best children’s hospital in the U.S. When I spoke with him on friday, he told me that one of the biggest challenges he faced daily was getting children to communicate their symptoms. Kids, especially those who were sick, scared, or in pain, often couldn’t or wouldn’t talk about what was wrong.

In response, his hospital had a dedicated system in place where patient care assistants, like my brother, would spend days at a time getting to know patients, building trust, and slowly extracting the critical health information needed for doctors to make informed decisions. But here’s the problem:

- 🚨 Most hospitals do not have the resources to do this.
- 🚨 Doctors don’t have the time to spend hours earning a child’s trust.
- 🚨 Missed or delayed diagnoses caused by communication gaps can be life-altering.

All children deserve a friend as approachable as my brother to communicate their medical needs. Ted Med is that solution. By combining AI, robotics, and best practices from literature, Ted helps kids open up about their symptoms in a way that feels natural, safe, and even fun—allowing doctors to focus on treatment rather than struggling to get answers.

This isn’t just about making hospitals less scary.
It’s about solving a real and urgent problem that affects millions of children every year.

## What It Does

Ted Med is a breakthrough **AI-powered interactive teddy bear** that redefines pediatric healthcare by transforming the way children communicate their health concerns. Designed to reduce anxiety, build trust, and enhance medical accuracy, Ted is more than just a companion—it’s a clinically intelligent assistant that helps doctors get the information they need from their youngest patients.

🧸 Ted Comforts & Engages Children in Natural Conversation
- Many children struggle to articulate symptoms due to shyness, fear, or developmental challenges. Ted bridges this gap by using emotionally aware dialogue and child-friendly interactions to encourage kids to open up about their feelings and health concerns.
- With speech recognition and animated responses, Ted feels like a real friend, reducing stress and creating a safe space for kids to communicate.
- Uses the CARE response method as outlined in Ruocco et al. 2019 to ensure kids feel supported and validated in their medical needs.

📋 Ted Gathers Crucial Medical Information
- When prompted by hospital staff, Ted doesn’t just chat randomly. He asks targeted, adaptive questions based on the needs of the medical staff to collect the life-saving qualitative data that can be nearly impossible to collect through traditional interviews and practices for some children.

🎭 Ted Reads Emotions & Adjusts Its Approach
- Leverages facial emotion detection (OpenCV, Mediapipe, DeepFace) enables Ted to sense emotions and adapt his responses accordingly.

📞 Ted Calls Caregivers for Follow-Ups
- For post-op check-in or if a child doesn’t fully articulate symptoms during the visit, Ted can call parents or caregivers later using Retell AI, ensuring that important medical insights aren’t lost after the appointment ends.
- Caregivers can provide additional details through voice or text, making pediatric consultations more comprehensive.

🛡 Ted Is the Safest AI for Kids – Rigorously Tested & Medically Verified
- Unlike general-purpose chatbots, Ted is engineered from the ground up for safety and accuracy.
- Harmful content detection: A fine-tuned RoBERTa discriminator model filters inappropriate or unsafe responses in real-time.
- Factual integrity: Retrieval-Augmented Generation (RAG) on medical response corpora ensures that Ted follows medical best practice.
- Benchmarked for safety: Ted was tested on MedSafetyBench & Aegis-AI-Content-Safety and decreased risk index by 60% on average. We also decreased Critical and High Risk Safety events to zero (n=900), only model to do so.

🚨 Ted Alerts Medical Staff If Something Is Wrong
- If a child says anything concerning (e.g., signs of abuse, self-harm, or alarming symptoms), Ted immediately flags the response for medical staff while handling the conversation with sensitivity.
- Ted ensures urgent health issues are escalated in real-time, preventing life-threatening conditions from being overlooked.

## How We Built It

🔹 Hardware: Raspberry Pi, Respeaker 4-Mic Array, Raspberry Pi Camera, Arduino Servo Motor
🔹 Software Stack:
- Frontend: React (Next.js, Tailwind, Vite) for a web dashboard for doctors & caregivers.
- Backend: FastAPI (Python) for processing and API services.
- AI & NLP:
- Retrieval-Augmented Generation (RAG) with LangChain for safer responses pulled from medical response corpora.
- Fine-tuned RoBERTa model for real-time content moderation.
- Text-to-Speech (Play.ht) for lifelike voice generation.
- Computer Vision (OpenCV, Mediapipe, DeepFace) for facial emotion analysis.
- Data Storage: Supabase (Vector DB) & AWS S3 for secure media storage.
- Phone Service: Retell AI for automated follow-ups with caregivers.

Challenges We Ran Into

- ⚠ Ensuring Content Safety: Designing an AI assistant for children required extreme care in filtering inappropriate content. Our discriminator model was fine-tuned and benchmarked on MedSafetyBench & Aegis-AI-Content-Safety.
- ⚠ Real-Time Processing on Edge Devices: Running AI models efficiently on a Raspberry Pi while maintaining low latency was a significant challenge. We optimized inference pipelines for edge deployment.

## Accomplishments That We’re Proud Of

- ✅ Built a robust, content safe AI system to **DO NO HARM** using fine-tuned NLP models and RAG for factual accuracy.
- ✅ Integrated real-time follow-up features to improve pediatric healthcare efficiency.
- ✅ Achieved real-time facial expression analysis to detect emotions and adjust Ted’s responses accordingly.

## What We Learned

- 📌 AI in pediatric healthcare must be built with rigorous safety checks—both in terms of content moderation and factual accuracy.
- 📌 Children interact with AI in unexpected ways, requiring adaptive and emotionally intelligent responses.
- 📌 Edge computing for AI-driven robotics is challenging but feasible with optimization.
- 📌 Doctors and caregivers value AI-assisted tools but need seamless integration into existing workflows.

## What’s Next for Ted Med

- 🚀 HIPAA Compliance & Clinical Trials – Work with healthcare institutions to ensure compliance and deploy Ted in real-world hospitals and clinics.
- 🚀 Emotionally Adaptive AI – Improve Ted’s facial emotion recognition and response system to dynamically adjust its tone, speech, and behavior based on a child’s emotional state.
- 🚀 Expanded Medical Integration – Direct integration with EHR systems to streamline medical record updates for pediatricians.
- 🚀 Scaling the Hardware – Develop smaller, more affordable versions of Ted for widespread adoption in hospitals and clinics worldwide.
