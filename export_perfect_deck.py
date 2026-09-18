import os
import sys
from playwright.sync_api import sync_playwright
from pptx import Presentation
from pptx.util import Inches
from PIL import Image

def generate_perfect_deck():
    html_path = os.path.abspath('index.html').replace('\\', '/')
    file_url = f'file:///{html_path}'
    output_dir = os.path.abspath('slide_exports')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Launching Chromium to render pixel-perfect slides...")
    
    slide_images = []
    
    with sync_playwright() as p:
        # Launch Chromium at 1920x1080 with 2x device scale factor (3840x2160 Ultra-HD / 4K crispness)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=2
        )
        page = context.new_page()
        page.goto(file_url, wait_until='networkidle')
        
        # Inject CSS to make deck-container fill the full 16:9 canvas cleanly
        page.add_style_tag(content="""
            .top-nav, .bottom-controls, #notes-drawer {
                display: none !important;
            }
            html, body {
                overflow: hidden !important;
                width: 100vw !important;
                height: 100vh !important;
                padding: 0 !important;
                margin: 0 !important;
                background: #0A0E15 !important;
            }
            .presentation-stage {
                padding: 0 !important;
                margin: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            .deck-container {
                width: 100vw !important;
                height: 100vh !important;
                max-width: 100vw !important;
                max-height: 100vh !important;
                border-radius: 0 !important;
                box-shadow: none !important;
                border: none !important;
            }
            .slide {
                transition: none !important;
                animation: none !important;
            }
        """)
        
        # Wait a moment for web fonts (Plus Jakarta Sans, Space Grotesk, Inter) to render
        page.wait_for_timeout(1000)
        
        speaker_notes = [
            # Slide 1
            "Good morning everyone! Quick question for the room—raise your hand if you plan on applying for software engineering, cloud, or AI roles in the next 1 to 2 years?\n\nRecruiters today look for two things: Hands-on Cloud experience, and real Generative AI applications built on enterprise platforms. Today, Amazon Web Services is officially launching AWS Builder Center on our campus. Over the next 6 minutes, I'm going to show you how to unlock official AWS training, free GenAI sandboxes, and a $100 certification exam voucher without paying a single rupee or entering a credit card.",
            
            # Slide 2
            "For those who don't know me, I'm Sathwik Bhat. I was selected by Amazon Web Services as the official AWS Student Builder Campus Leader (SBCL) for our college.\n\nMy role here this semester is very simple: I am not here to sell you any paid course. Everything I share is 100% free. My role is to act as the direct link between Amazon's engineering teams and our classrooms. Over the next few weeks, I'll be running hands-on cloud labs, Generative AI workshops, hackathon mentoring, and directly nominating active students from our college to receive official AWS exam vouchers and credits. You can see my verified profile on the screen at @bhatsathwik.",
            
            # Slide 3
            "So what actually is AWS Builder Center?\n\nMost of us only know about the standard AWS Console—which asks for an international credit card and gives you anxiety about accidental billing. Builder Center is completely different.\n\nAmazon built builder.aws.com as an official developer hub and project sandbox. Think of it as a hybrid between GitHub, Medium, and an AWS cloud playground:\n1. Real-world architectures by Amazon Principal Engineers.\n2. Instant GenAI sandboxes with PartyRock and Amazon Q Developer.\n3. A permanent public portfolio at builder.aws.com/@your_alias that recruiters notice.",
            
            # Slide 4
            "Now look at this slide carefully. What Amazon has rolled out for universities is not just a basic free tier. It is an official student package worth up to $579—that is over ₹48,000 rupees in enterprise resources—given to us for free.\n\n1. Official Learning Tracks ($449 Value): An annual subscription to AWS Skill Builder normally costs $449/year (₹38,000) for industry professionals. Through our campus student onboarding and SheerID verification, you unlock the entire curriculum, hands-on labs, and interactive 3D Cloud Quest for free.\n2. Student Rewards ($100 Exam Voucher + Credits): The official AWS Cloud Practitioner certification exam costs $100 (~₹8,500). By earning community badges on Builder Center, you unlock direct AWS cloud credits and qualify for a $100 exam voucher to get certified without paying out of pocket.\n3. AI Innovation (PartyRock & Amazon Q): Build and share prompt-powered GenAI apps in seconds using PartyRock on Amazon Bedrock—no paid API keys needed. Plus get Amazon Q Developer inside VS Code.\n4. Verified Profile & Campus Network: Your projects live on builder.aws.com/@alias. Plus, join our campus study circles.\n5. Bottom Banner: No credit cards, no international debit cards, no accidental billing. It's powered by AWS Builder ID in 60 seconds.",
            
            # Slide 5
            "Everyone, take out your phones right now. We are going to lock in your handles together in literally 45 seconds.\n\nHere is the exact 4-step flow shown on screen:\n- Step 1: Tap 'Sign in' at the top right and enter your email to create your AWS Builder ID.\n- Step 2: Once signed in, tap the Back Arrow (<) at the top left to open the handle setup page.\n- Step 3: Claim your unique @alias. Keep it professional—use your name or developer handle. Select Country: India.\n- Step 4: Select 'Yes' for Student status, choose your branch and graduation year. This is what unlocks your student benefits and the $449 Skill Builder access.",
            
            # Slide 6
            "Scan this QR code on screen right now, or open bit.ly/4hQ40lk in your phone browser.\n\nOnce you claim your @alias, there is one final 20-second step: Fill our campus Verification Form. Enter your Name, USN, and your new @alias.\n\nWhy is this important? Because this sheet is my official campus whitelist. When AWS allocates $100 certification exam vouchers, workshop seats, and project credits to our college, I distribute them directly to the verified students on this list.\n\nAs soon as you submit the form, it will show you the link to join our campus AWS WhatsApp Community. I'll give everyone 90 seconds right now to finish. If anyone's phone gets stuck, raise your hand and I'll come over right now to help!"
        ]
        
        for i in range(1, 7):
            # Activate slide i
            page.evaluate(f"""
                () => {{
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach((s) => {{
                        if (parseInt(s.dataset.slide, 10) === {i}) {{
                            s.classList.add('active');
                            s.style.display = 'flex';
                            s.style.opacity = '1';
                        }} else {{
                            s.classList.remove('active');
                            s.style.display = 'none';
                            s.style.opacity = '0';
                        }}
                    }});
                }}
            """)
            page.wait_for_timeout(500)
            img_path = os.path.join(output_dir, f"slide_{i}.png")
            page.screenshot(path=img_path)
            slide_images.append(img_path)
            print(f"Rendered Slide {i} -> {img_path}")
            
        browser.close()
        
    print("\nAssembling PowerPoint Presentation (.pptx)...")
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    for idx, img_path in enumerate(slide_images):
        slide = prs.slides.add_slide(blank_layout)
        # Add full bleed 16:9 picture (0 margins, full resolution)
        slide.shapes.add_picture(img_path, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
        
        # Add speaker notes to the slide!
        if idx < len(speaker_notes):
            notes_slide = slide.notes_slide
            tf = notes_slide.notes_text_frame
            tf.text = speaker_notes[idx]
            
    pptx_filename = "AWS_Builder_Center_Class_Announcement.pptx"
    prs.save(pptx_filename)
    print(f"SUCCESS: Saved pristine PowerPoint to: {os.path.abspath(pptx_filename)}")
    
    # Also create a high-definition PDF
    pdf_filename = "AWS_Builder_Center_Class_Announcement.pdf"
    pil_images = [Image.open(img).convert("RGB") for img in slide_images]
    if pil_images:
        pil_images[0].save(
            pdf_filename,
            save_all=True,
            append_images=pil_images[1:],
            quality=95
        )
        print(f"SUCCESS: Saved pristine PDF deck to: {os.path.abspath(pdf_filename)}")

if __name__ == "__main__":
    generate_perfect_deck()
