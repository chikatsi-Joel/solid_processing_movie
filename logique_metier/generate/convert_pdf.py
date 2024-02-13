from reportlab.pdfgen import canvas

class convertir:
    @staticmethod
    def convert_srt_en_pdf(pdf_path : str, srt_path : str):
        pdf = canvas.Canvas(pdf_path)
        with open(srt_path, 'r') as file:
            lines = file.readlines()
        y = 700 
        num_lines_added = 0 
        pdf.drawString(250, 800, "VIDEO PROCESSING")
        while num_lines_added < len(lines):
            line = lines[num_lines_added].strip()
            if line.isdigit() or '-->' in line or line == '':
                num_lines_added += 1
                continue

            pdf.drawString(50, y, line)
            y -= 20 
            num_lines_added += 1

            if y < 50:
                pdf.showPage()
                y = 800

        pdf.save()



