import pandas as pd
from PIL import Image
import streamlit as st
# from transform import toDot
from streamlit_drawable_canvas import st_canvas

# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ( "freedraw", "line", "transform")    #("point", "freedraw", "line", "rect", "circle", "transform")  
)

stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
# if drawing_mode == 'point':
#     point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ")
bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
bg_image = st.file_uploader("Background image:", type=["png", "jpg"])
dot = st.slider(value=5,min_value=1,max_value=20, label="dot")

if bg_image==None:
    
    st.info("그림을 업로드하세요")
else:  
    r = Image.open(bg_image)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=r if bg_image else None,
        width=r.size[0],
        
        # update_streamlit=realtime_update,
        height=r.size[1],
        drawing_mode=drawing_mode,
        # point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        key="canvas",
    )
    
    r_new = Image.open(bg_image)
    
    m_size = dot   # 모자이크 크기 10
    x_m =r_new.size[0] % m_size
    y_m =r_new.size[1] % m_size
    x_p = m_size - x_m
    y_p = m_size - y_m
    r_new = Image.new(r_new.mode, (r_new.size[0]+x_p, r_new.size[1]+y_p),(255,255,255))
    r_new.paste(r, (0,0))

    for i in range(0, r_new.size[0],m_size):
        for j in range(0, r_new.size[1],m_size):
            r_sum = 0
            g_sum = 0
            b_sum = 0
            for ii in range(i, i+m_size):
                for jj in range(j, j+m_size):
                    rgb = r_new.getpixel((ii,jj))
                    r_sum += rgb[0]
                    g_sum += rgb[1]
                    b_sum += rgb[2]
            r_a = round(r_sum/m_size**2) # rgb 평균 구하기
            g_a = round(g_sum/m_size**2)
            b_a = round(b_sum/m_size**2)
            ##### 이 사이에 코드 추가 #####
            for ii in range(i, i+m_size):
                for jj in range(j, j+m_size):
                    r_new.putpixel((ii,jj),(r_a,g_a,b_a)) # rgb 평균 구해서 색깔 집어 넣기


    canvas_result1 = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    background_image=r_new if r_new else None,
    width=r_new.size[0],
    # update_streamlit=realtime_update,
    height=r_new.size[1],
    # point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas2",
    )

# # Do something interesting with the image data and paths
# if canvas_result.image_data is not None:
#     st.image(canvas_result.image_data)
# if canvas_result.json_data is not None:
#     objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
#     for col in objects.select_dtypes(include=['object']).columns:
#         objects[col] = objects[col].astype("str")
#     st.dataframe(objects)