from PIL import Image, ImageDraw
class Font:
    def __init__(self):
        l = "ABCDEFGHIJKLMNOPQRSTUVWXYZpeqctlrd1234567890"
        img = Image.open("sprites/font.png")
        print(img.size)
        row = 0
        col = 0
        empty_rows = []
        matrix = []
        curr_row = []
        empty_row = True
        for pixel in img.getdata():
            
            if pixel != (0,0,0,0):
                empty_row = False
            curr_row.append(pixel)
            col+=1
            if col == 64:
                if empty_row:
                    empty_rows.append(row)
                col = 0
                row+=1
                empty_row = True
                matrix.append(curr_row)
                curr_row = []
            
        i = 0
        count = 0
        print(len(matrix[i]))
        print(len(matrix[i+1]))
        while i < len(matrix):
            j = 0
            if i in empty_rows:
                i+=1
                continue
            empty_cols = []
            while j < len(matrix[i]):

                empty_col = True
                for k in range(7):
                    row = i+k
                    if matrix[row][j] != (0,0,0,0):
                        empty_col = False
                if empty_col:
                    empty_cols.append(j)
                j+=1
            
            j = 0
            print(empty_cols)
            while(empty_cols):
                
                next_col = empty_cols.pop(0)
                if next_col == 63:
                        print(i,holder,"here")
                
                while j == next_col:
                    next_col = empty_cols.pop(0)
                
                img = Image.new("RGBA", (7, 7), (0,0,0,0))  
                draw = ImageDraw.Draw(img)
                write = False
                j = j+1
                for k in range(7):
                    
                    holder = j
                   
                    if next_col == 63:
                        print(i,holder,"here")
                    while holder < next_col:
                        row = i+k
                        
                        if matrix[row][holder] != (0,0,0,0):
                            draw.point((holder-j,k), fill=matrix[row][holder])
                            write = True
                        holder+=1
                
                if write:
                    img.save(f"sprites/font/{l[count]}.png")
                    count+=1
                    
                
                j = next_col

            i+=7
                

            




        


if __name__ == "__main__":
    font = Font()
    print("Font loaded.")
    