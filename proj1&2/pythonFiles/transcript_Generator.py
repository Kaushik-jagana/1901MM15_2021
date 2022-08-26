def generate_transcript():
    import fpdf
    import csv
    import datetime
    import os
    import shutil
    import sys

    if not os.path.exists(f"public//sample_input//grades.csv"):
        print(f"please upload grades.csv file")
        exit()
    if not os.path.exists(f"public//sample_input//names-roll.csv"):
        print(f"please upload names-roll.csv file")
        exit()
    if not os.path.exists(f"public//sample_input//subjects_master.csv"):
        print(f"please upload subjects_master.csv file")
        exit()

    all, nlst, flag = int(sys.argv[3]), [], 0
    stmp, sgn = sys.argv[4], sys.argv[5]
    r_from, r_upto = sys.argv[1].upper().strip().strip(
        "'"), sys.argv[2].upper()
    with open(r"public//sample_input//names-roll.csv", 'r') as file:
        rows = csv.reader(file)
        rlnm = {line[0]: line[1].strip() for line in rows if line[0] != "Roll"}
        ordlst = sorted(rlnm.keys())

    if(not all):
        if(not(r_from[6:].isnumeric() and r_upto[6:].isnumeric())):
            print(f"Please give valid input like '{ordlst[0]}'")
            exit()
        if(r_from[:6] == r_upto[:6]):
            nlst = [f"{r_from[:6]}{str((int(r_from[6:])+i)).zfill(2)}" for i in range(
                int(r_upto[6:])-int(r_from[6:])+1)]
        else:
            flag = 1
    if os.path.exists("transcriptsIITP"):
        shutil.rmtree("transcriptsIITP")
    if os.path.exists("tmp_csv_output"):
        shutil.rmtree("tmp_csv_output")
    os.makedirs("transcriptsIITP")
    os.makedirs("tmp_csv_output")
    with open(r"public//sample_input//subjects_master.csv", 'r') as file:
        rows = csv.reader(file)
        sbj = {line[0]: [line[1], line[2]]
               for line in rows if line[0] != "subno"}
    rplc = {"AA": "10", "AB": "9", "BB": "8", "BC": "7",
            "CC": "6", "CD": "5", "DD": "4", "F": "0", "I": "0"}
    u = {i: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in rlnm}
    s = {i: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in rlnm}
    f = {i: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in rlnm}
    with open(r"public//sample_input//grades.csv", 'r') as file:
        rows = csv.reader(file)
        for line in rows:
            if line[0] == 'Roll':
                continue
            s[line[0]][int(line[1])] = s[line[0]][int(line[1])]+int(line[3])
            if(line[4].strip().strip("*") == "F" or line[4].strip().strip("*") == "I"):
                f[line[0]][int(line[1])] = f[line[0]
                                             ][int(line[1])] + int(line[3])
            u[line[0]][int(line[1])] = u[line[0]][int(line[1])] + \
                int(line[3])*int(rplc[line[4].strip().strip("*")])
            if(not os.path.isfile(f"tmp_csv_output//{line[0]}_{line[1]}.csv")):
                with open(f"tmp_csv_output//{line[0]}_{line[1]}.csv", "a", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        ["Sub. Code", "Subject Name", "L-T-P", "CRD", "GRD"])
            with open(f"tmp_csv_output//{line[0]}_{line[1]}.csv", "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([line[2], sbj[line[2]][0],
                                sbj[line[2]][1], line[3], line[4]])
    r = {key: [i for i, el in enumerate(s[key]) if el != 0] for key in rlnm}
    cry = {"CS": "Computer Science and Engineering", "ME": "Mechanical engineering",
           "EE": "Electrical and Electronics Engineering", "04": "2004", "05": "2005"}

    class PDF(fpdf.FPDF):
        def improved_table(self, i, el, key, row, col_widths=(15, 70, 15, 9, 9)):
            self.set_xy(25+125*(i % 3), 60+65*(i//3))
            self.set_font('Helvetica', 'BU', 8)
            self.cell(20, 4, f"Semester {r[key][i]}", 0, 1, "L")
            for j, row in enumerate(rows):
                self.set_font('Helvetica', '', 8)
                if(j == 0):
                    self.set_font('Helvetica', 'B', 8)
                self.set_x(25+(i % 3)*125)
                self.cell(col_widths[0], 4, row[0], 1, 0, "C")
                self.cell(col_widths[1], 4, row[1], 1, 0, "C")
                self.cell(col_widths[2], 4, row[2], 1, 0, "C")
                self.cell(col_widths[3], 4, row[3], 1, 0, "C")
                self.set_font('Helvetica', 'B', 8)
                self.cell(col_widths[4], 4, row[4], 1, 1, "C")
            self.cell(2, 1, "", 0, 1)
            self.set_x(35+(i % 3)*125)
            tot = f"Credits Taken: {s[key][el]}    Credits Cleared: {s[key][el]-f[key][el]}    SPI: {round(u[key][el]/s[key][el], 2)}    CPI: {round(sum(u[key][:el+1])/sum(s[key][:el+1]), 2)}"
            self.cell(92, 5, tot, 1, 0, "C")

    for key in ordlst:
        if((not all) and key > r_upto):
            break
        if(all or key >= r_from):
            pdf = PDF('L', 'mm', 'A3')
            pdf.add_page()
            pdf.set_font('Helvetica', 'BU', 9)
            pdf.set_xy(32, 37)
            pdf.cell(1, 0, "INTERIM TRANSCRIPT", 0, 0, "C")
            pdf.set_xy(387, 37)
            pdf.cell(1, 0, "INTERIM TRANSCRIPT", 0, 0, "C")
            pdf.set_xy(209, 36)
            pdf.set_font('Courier', 'B', 20)
            pdf.cell(1, 0, "TRANSCRIPT", 0, 0, "C")
            pdf.rect(10, 10, 400, 277)
            pdf.rect(10, 40, 400, 80)
            pdf.rect(55, 10, 310, 30)
            pdf.rect(83, 42, 250, 15)
            if(len(r[key]) > 3):
                pdf.rect(10, 120, 400, 65)
            if(len(r[key]) > 6):
                pdf.rect(10, 185, 400, 65)
            pdf.set_font('Helvetica', '', 8)
            pdf.set_xy(49, 270)
            pdf.cell(1, 0, datetime.datetime.now().strftime("%d %b %Y, %H:%M"))
            for i, el in enumerate([f"{key}", "Bachelor of Technology", f"{rlnm[key]}", cry[key[4:6]], cry[key[:2]]]):
                pdf.set_xy(108+i//2*72+i//4*51, 46+i % 2*6)
                pdf.cell(1, 0, el)
            pdf.set_font('Helvetica', 'B', 8)
            for i, el in enumerate(["Roll No:", "Programme:", "Name:", "Course:", "Year of Admission:"]):
                pdf.set_xy(90+i//2*78+i//4*30, 46+i % 2*6)
                pdf.cell(1, 0, f"{el}")
            pdf.set_xy(25, 270)
            pdf.cell(1, 0, f"Date Generated:  _________________")
            pdf.set_xy(285, 270)
            pdf.cell(1, 0, "Assistant Registrar(Academic):   ___________________")
            pdf.image("public//logo.jpg", 23, 12, 20, 20)
            pdf.image("public//logo.jpg", 378, 12, 20, 20)
            pdf.image("public//title.jpg", 83, 11, 250, 20)
            if stmp != "" and os.path.exists(f"public//sample_input//{stmp}"):
                pdf.image(f"public//sample_input//{stmp}", 185, 255, 25, 25)
            if sgn != "" and os.path.exists(f"public//sample_input//{sgn}"):
                pdf.image(f"public//sample_input//{sgn}", 330, 254, 65, 20)
            for i, el in enumerate(r[key]):
                with open(f"tmp_csv_output//{key}_{el}.csv", 'r') as file:
                    rows = csv.reader(file)
                    pdf.improved_table(i, el, key, rows)
            pdf.output(f'transcriptsIITP//{key}.pdf')
            if (not all):
                if(key in nlst):
                    nlst.remove(key)
    shutil.rmtree("tmp_csv_output")
    stro = ""
    if(not all):
        if(len(nlst) > 9):
            stro += "Transcripts of roll numbers "
            for i in range(7):
                stro += f"{nlst[i]}, "
            stro += f" and {len(nlst)-7} more are not generated"
        elif(len(nlst) == 0):
            if(flag == 0):
                stro += "All transcripts in the range are generated"
            else:
                stro += "Some transcripts in the range are not generated"
        else:
            stro += "Transcripts of roll numbers "
            for i in range(len(nlst)):
                stro += f"{nlst[i]}, "
            stro += f" are not generated"
        stro.strip(", ")
        print(stro)
    else:
        print("All transcripts are generated")
    shutil.make_archive("transcriptsIITP", 'zip', "transcriptsIITP")
    return


generate_transcript()
