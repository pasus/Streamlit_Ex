# 

import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode

st.set_page_config(page_title="Aircraft Sizing", page_icon="📈", layout="wide")

# Sidebar ------------------------------------------------
# 1. 제목
st.sidebar.write("## ✈️  Mission Requirements")
st.sidebar.write(" ")

# 2. 항속거리
col1, col2, col3 = st.sidebar.columns([2, 2, 1])
with col1:
    st.text("Range")
with col2:
    range_input = st.text_input("Range", value="15", label_visibility="collapsed")
with col3:
    st.markdown("*km*")

try:
    range_km = float(range_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter a valid number.")

# 3. 항속시간
col1, col2, col3 = st.sidebar.columns([2, 2, 1])
with col1:
    st.text("Endurance")
with col2:
    endurance_input = st.text_input("Endurance", value="10", label_visibility="collapsed")
with col3:
    st.markdown("*min*")
try:
    endurance_min = float(endurance_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter a valid number.")

# 4. 최소속력
col1, col2, col3 = st.sidebar.columns([2, 2, 1])
with col1:
    st.text("Min Speed")
with col2:
    min_speed_input = st.text_input("Min Speed", value="10", label_visibility="collapsed")
with col3:
    st.markdown("*m/sec*")
try:
    min_speed_ms = float(min_speed_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter a valid number.")


# 5. stall 마진
col1, col2, col3 = st.sidebar.columns([2, 2, 1])
with col1:
    st.text("Stall Margin")
with col2:
    stall_margin_input = st.text_input("Stall Margin", value="7", label_visibility="collapsed")
with col3:
    st.markdown("*m/sec*")
try:
    stall_margin_ms = float(stall_margin_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter a valid number.")

# 6. 페이로드
col1, col2, col3 = st.sidebar.columns([2, 2, 1])
with col1:
    st.text("Payload")
with col2:
    payload_input = st.text_input("Payload", value="1", label_visibility="collapsed")
with col3:
    st.markdown("*kg*")
try:
    payload_kg = float(payload_input)
except ValueError:
    st.sidebar.error("⚠️ Please enter a valid number.")



# Main ------------------------------------------------
# 7. 제목
st.title("Simple Aircraft Sizing")
st.write(
    """
    **Designed by Sejong FDC Lab**
    """
)
st.write(" ")


# 8. 설계 파라미터 입력
st.write("### ✅  Design Parameters")
st.write(" ")

# ==============================
#  Wing + Airframe SECTION
# ==============================
st.markdown("**🍎  Wing_Airframe**")
with st.expander("Enter Design Parameters", expanded=False):
    df_af = pd.DataFrame({
        "Airframe": ["Weight (kg)", "Fuselage Drag Coeff"],
        "Values": [5, 0.03]
    })

    gb_af = GridOptionsBuilder.from_dataframe(df_af)
    gb_af.configure_column("Airframe", editable=False, width=430)
    gb_af.configure_column("Values", editable=True, type=["numericColumn"], 
                             precision=3, width=150)
    grid_options_af = gb_af.build()

    grid_response_af = AgGrid(
            df_af,
            gridOptions=grid_options_af,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            theme="streamlit",
            fit_columns_on_grid_load=True,
            height=105,
            enable_enterprise_modules=False,
            allow_unsafe_jscode=True
        )
    updated_df_af = grid_response_af["data"]

    W_emp = float(updated_df_af.iloc[0]["Values"])
    cd_0f = float(updated_df_af.iloc[1]["Values"])


    df_wing = pd.DataFrame({
        "Wing": ["Wing Loading (g/cm²)", "Aspect Ratio", "Max. C_L", "C_D0",
                       "Taper Ratio", "Oswald Efficiency"],
        "Values": [50.0, 8.0, 1.12, 0.015, 1.0, 0.85]
    })

    gb_wing = GridOptionsBuilder.from_dataframe(df_wing)
    gb_wing.configure_column("Wing", editable=False, width=430)
    gb_wing.configure_column("Values", editable=True, type=["numericColumn"], 
                             precision=3, width=150)
    grid_options_wing = gb_wing.build()

    grid_response_wing = AgGrid(
            df_wing,
            gridOptions=grid_options_wing,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            theme="streamlit",
            fit_columns_on_grid_load=True,
            height=220,
            enable_enterprise_modules=False,
            allow_unsafe_jscode=True
        )
    updated_df_wing = grid_response_wing["data"]

    wing_loading = float(updated_df_wing.iloc[0]["Values"])
    aspect_ratio = float(updated_df_wing.iloc[1]["Values"])
    cl_max = float(updated_df_wing.iloc[2]["Values"])
    cd_0 = float(updated_df_wing.iloc[3]["Values"])
    taper_ratio = float(updated_df_wing.iloc[4]["Values"])
    oswald_eff = float(updated_df_wing.iloc[5]["Values"])


# ==============================
# Tail SECTION
# ==============================
st.markdown("**🍑  Tail**")
with st.expander("Enter Design Parameters", expanded=False):
   
    df_hor = pd.DataFrame({
        "Horizontal": ["Volume Ratio", "Moment Arm (m)", "Aspect Ratio", "Taper Ratio"],
        "Values": [0.4, 1.0, 1.0, 1.0]
    })

    df_ver = pd.DataFrame({
        "Vertical": ["Volume Ratio", "Moment Arm (m)", "Span (m)", "Taper Ratio"],
        "Values": [0.03, 1.0, 1.0, 1.0]
    })
    
    gb_hor = GridOptionsBuilder.from_dataframe(df_hor)
    gb_hor.configure_column("Horizontal", editable=False, width=430)
    gb_hor.configure_column("Values", editable=True, type=["numericColumn"], 
                            precision=3, width=150)
    grid_options_hor = gb_hor.build()

    grid_response_hor = AgGrid(
            df_hor,
            gridOptions=grid_options_hor,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            theme="streamlit",
            fit_columns_on_grid_load=True,
            height=160,
            enable_enterprise_modules=False,
            allow_unsafe_jscode=True
        )

    updated_df_hor = grid_response_hor["data"]

    gb_ver = GridOptionsBuilder.from_dataframe(df_ver)
    gb_ver.configure_column("Vertical", editable=False, width=430)
    gb_ver.configure_column("Values", editable=True, type=["numericColumn"], 
                            precision=3, width=150)
    grid_options_ver = gb_ver.build()

    grid_response_ver = AgGrid(
            df_ver,
            gridOptions=grid_options_ver,
            update_mode=GridUpdateMode.VALUE_CHANGED,
            theme="streamlit",
            fit_columns_on_grid_load=True,
            height=160,
            enable_enterprise_modules=False,
            allow_unsafe_jscode=True
        )
    updated_df_ver = grid_response_ver["data"]
    
    volume_ratio_H = float(updated_df_hor.iloc[0]["Values"])
    moment_arm_H = float(updated_df_hor.iloc[1]["Values"])
    aspect_ratio_H = float(updated_df_hor.iloc[2]["Values"])
    taper_ratio_H = float(updated_df_hor.iloc[3]["Values"])

    volume_ratio_V = float(updated_df_ver.iloc[0]["Values"])
    moment_arm_V = float(updated_df_ver.iloc[1]["Values"])
    b_V = float(updated_df_hor.iloc[2]["Values"])
    taper_ratio_V = float(updated_df_ver.iloc[3]["Values"])

# ==============================
# Battery / Power / Propulsion SECTION
# ==============================

st.markdown("**🔋   Battery | Power | Propulsion**")
with st.expander("Provide Battery Specifications", expanded=False):
    df_bat = pd.DataFrame({
        "Battery": ["Battery Pack Capacity (mAh)", "Energy density (W-h/kg)", 
                    "Cell Voltage (V)", "Number of Cell (#N)", "Number of Baterries (#N)", 
                    "Capacity Used (%)", "Overall Efficiency (%)"],
        "Values": [27000, 135, 3.7, 6, 1, 80, 40]
    })

    gb_bat = GridOptionsBuilder.from_dataframe(df_bat)
    gb_bat.configure_column("Battery", editable=False, width=430)
    gb_bat.configure_column("Values", editable=True, type=["numericColumn"], 
                             precision=3, width=150)
    grid_options_bat = gb_bat.build()

    grid_response_bat = AgGrid(
        df_bat,
        gridOptions=grid_options_bat,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        theme="streamlit",
        fit_columns_on_grid_load=True,
        height=250,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True
    )
    updated_df_bat = grid_response_bat["data"]

    bat_pack_cap = float(updated_df_bat.iloc[0]["Values"])
    bat_energy_density = float(updated_df_bat.iloc[1]["Values"])
    bat_cell_volt = float(updated_df_bat.iloc[2]["Values"])
    bat_num_cell = float(updated_df_bat.iloc[3]["Values"])
    bat_num_bat = float(updated_df_bat.iloc[4]["Values"])
    bat_cap_useed = float(updated_df_bat.iloc[5]["Values"])
    efficiency = float(updated_df_bat.iloc[6]["Values"])

    df_pow = pd.DataFrame({
        "Power": ["Payload Power (W)", "Avionics Power (W)"],
        "Values": [0, 0]
    })

    gb_pow = GridOptionsBuilder.from_dataframe(df_pow)
    gb_pow.configure_column("Power", editable=False, width=430)
    gb_pow.configure_column("Values", editable=True, type=["numericColumn"], 
                             precision=3, width=150)
    grid_options_pow = gb_pow.build()

    grid_response_pow = AgGrid(
        df_pow,
        gridOptions=grid_options_pow,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        theme="streamlit",
        fit_columns_on_grid_load=True,
        height=100,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True
    )
    updated_df_pow = grid_response_pow["data"]


    payload_power = float(updated_df_pow.iloc[0]["Values"])
    avionics_power = float(updated_df_pow.iloc[1]["Values"])


# 9. 사이징 계산
st.markdown("**✈️   Enter Cruse Speed (m/sec)**")
cruise_input = st.text_input("Cruise Speed (m/sec)", value="25", label_visibility="collapsed")
try:
    cruise_ms = float(cruise_input)
except ValueError:
    st.error("⚠️ Please enter a valid number.")

rho = 1.225 # kg/m^3

# battery
total_battery_cap = bat_pack_cap * bat_num_bat  # mAh 
total_volt = bat_cell_volt * bat_num_cell 

# weight
W_bat = total_battery_cap*total_volt*0.001 / bat_energy_density
W_total = W_bat + W_emp + payload_kg # kg
W_frac = (W_bat+payload_kg) / W_total


# main wing
S_wing = W_total*10 / wing_loading # m^2
b_wing = np.sqrt(S_wing*aspect_ratio) # m
c_wing_m = S_wing / b_wing
c_wing_r = 2*S_wing / (b_wing*(1+taper_ratio))
c_wing_t = c_wing_r * taper_ratio


# horizontal tail
S_H = volume_ratio_H * c_wing_m * S_wing / moment_arm_H # m^2
b_H = np.sqrt(S_H*aspect_ratio_H) # m
c_H_m = S_H / b_H
c_H_r = 2*S_H / (b_H*(1+taper_ratio_H))
c_H_t = c_H_r * taper_ratio_H

# vertical tail
S_V = volume_ratio_V * b_wing * S_wing / moment_arm_V # m^2
c_V_m = S_H / b_V
c_V_r = 2*S_V / (b_V*(1+taper_ratio_V))
c_V_t = c_V_r * taper_ratio_V

# velocity
V_min = np.sqrt(2/cl_max) * np.sqrt(W_total*9.8/(rho*S_wing)) # m/sec
V_drag = np.sqrt(2) / (np.pi*oswald_eff*aspect_ratio*(cd_0+cd_0f))**(1/4) * np.sqrt(W_total*9.8/(rho*S_wing)) # m/sec
V_power = 2 / (12*np.pi*oswald_eff*aspect_ratio*(cd_0+cd_0f))**(1/4) * np.sqrt(W_total*9.8/(rho*S_wing)) # m/sec
V_margin = cruise_ms - V_min

# aerodynamic coefficients
C_L = 2 * W_total*9.8 / (rho * cruise_ms**2 * S_wing)
C_D = cd_0 + cd_0f + C_L**2/(np.pi*oswald_eff*aspect_ratio)
L2DR = C_L / C_D

# power
P_req = W_total * 9.8 * cruise_ms / (efficiency*0.01*L2DR) # Watt
current_req = P_req / total_volt # A

# estimated endurance and range
current_extra = (payload_power + avionics_power) / total_volt
tof = total_battery_cap*0.001 * bat_cap_useed*0.01 / (current_req + current_extra) * 60 # min
rof = tof*60 * cruise_ms * 0.001 # km


# 10. 임무요구조건 충족 확인 
results_df = pd.DataFrame({
    "Parameter": ["Range", "Endurance", "Min Speed", "Stall Margin"],
    "Value": [rof, tof, V_min, V_margin],
    "Unit": ["km", "min", "m/s", "m/s"]
})

cell_style_jscode = JsCode(f"""
    function(params) {{
        const val = params.value;
        const param = params.data.Parameter;

        if (param === 'Range' && val < {range_km}) {{
            return {{ backgroundColor: '#fff3cd' }};  // 연노랑
        }}
        if (param === 'Endurance' && val < {endurance_min}) {{
            return {{ backgroundColor: '#fff3cd' }};
        }}
        if (param === 'Min Speed' && val > {min_speed_ms}) {{
            return {{ backgroundColor: '#fff3cd' }};
        }}
        if (param === 'Stall Margin' && val < {stall_margin_ms}) {{
            return {{ backgroundColor: '#fff3cd' }};
        }}
        return null;
    }}
    """)

gb = GridOptionsBuilder.from_dataframe(results_df)
gb.configure_column("Parameter", editable=False)
gb.configure_column("Unit", editable=False)
gb.configure_column(
    "Value",
    editable=False,
    type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
    precision=2,
    cellStyle=cell_style_jscode
)
grid_options = gb.build()

st.write(" ")
st.markdown("### ✅ Mission Compliance Check")
AgGrid(
    results_df,
    gridOptions=grid_options,
    theme="streamlit",
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    height=200
)


# 11. 결과 표시 
st.write(" ")
st.markdown("### ✅ Sizing Results")

#  Wing + Airframe SECTION ==============================

st.markdown("**🍎  Wing_Airframe**")
w_data = [
    ("W_empty", W_emp, "kg"),
    ("W_payload", payload_kg, "kg"),
    ("P_payload", payload_power, "W"),
    ("P_avionics", avionics_power, "W"),
    ("WS_ratio", wing_loading, "g/cm²"),
    ("AR", aspect_ratio, ""),
    ("TR", taper_ratio, ""),
    ("C_D0_f", cd_0f, ""),
    ("C_D0", cd_0, ""),
    ("C_L_max", cl_max, ""),
    ("Oswald", oswald_eff, ""),
    ("Sw", S_wing, "m²"),
    ("bw", b_wing, "m"),
    ("cw_m", c_wing_m, "m"),
    ("cw_r", c_wing_r, "m"),
    ("cw_t", c_wing_t, "m")
]

#
df_wb = pd.DataFrame(w_data, columns=["Parameter", "Value", "Unit"])
df_wb["Value"] = df_wb["Value"].map(lambda x: f"{x:.2f}")
#
half = len(df_wb) // 2 + len(df_wb) % 2
df_left = df_wb.iloc[:half].reset_index(drop=True)
df_right = df_wb.iloc[half:].reset_index(drop=True)
#
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_left, hide_index=True, use_container_width=True)
with col2:
    st.dataframe(df_right, hide_index=True, use_container_width=True)


#  Tail SECTION ==============================

st.markdown("**🍑  Tail**")

h_data = [
    ("V_H", volume_ratio_H , ""),
    ("l_H", moment_arm_H, "m"),
    ("AR_H", aspect_ratio_H, ""),
    ("TR_H", taper_ratio_H, ""),
    ("Sh", S_H, "m²"),
    ("bh", b_H, "m"),
    ("ch_m", c_H_m, "m"),
    ("ch_r", c_H_r, "m"),
    ("ch_t", c_H_t, "m")
]

v_data = [
    ("V_V", volume_ratio_V , ""),
    ("l_V", moment_arm_V, "m"),
    ("bv", b_V, "m"),
    ("TR_H", taper_ratio_V, ""),
    ("Sv", S_V, "m²"),
    ("cv_m", c_V_m, "m"),
    ("cv_r", c_V_r, "m"),
    ("cv_t", c_V_t, "m")
]

#
df_th = pd.DataFrame(h_data, columns=["Parameter", "Value", "Unit"])
df_th["Value"] = df_th["Value"].map(lambda x: f"{x:.2f}")
df_tv = pd.DataFrame(v_data, columns=["Parameter", "Value", "Unit"])
df_tv["Value"] = df_tv["Value"].map(lambda x: f"{x:.2f}")
#
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_th, hide_index=True, use_container_width=True)
with col2:
    st.dataframe(df_tv, hide_index=True, use_container_width=True)

#  Battery Power SECTION ==============================

st.markdown("**🔋   Battery | Power**")

p_data = [
    ("Q_cell", bat_pack_cap, "mAh"),
    ("rho_energy", bat_energy_density, "Wh/kg"),
    ("V_cell", bat_cell_volt, "V"),
    ("N_cell", bat_num_cell, ""),
    ("N_battery", bat_num_bat, ""),
    ("Q_total", total_battery_cap, "mAh"),
    ("V_total", total_volt, "V"),
    ("W_battery", W_bat, "kg"),
    ("eta_Qused", bat_cap_useed, "%"),
    ("eta_all", efficiency, "%"),
    ("P_req", P_req, "W"),
    ("I_req", current_req, "A")
]

#
df_p = pd.DataFrame(p_data, columns=["Parameter", "Value", "Unit"])
def format_value(row):
    if row["Parameter"] in ["N_cell", "N_battery"]:
        return f"{int(row['Value'])}"
    else:
        return f"{row['Value']:.2f}"

df_p["Value"] = df_p.apply(format_value, axis=1)
#
halfp = len(df_p) // 2 + len(df_p) % 2
df_leftp = df_p.iloc[:halfp].reset_index(drop=True)
df_rightp = df_p.iloc[halfp:].reset_index(drop=True)
#
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_leftp, hide_index=True, use_container_width=True)
with col2:
    st.dataframe(df_rightp, hide_index=True, use_container_width=True)


# Performance SECTION ==============================

st.markdown("**✈️  Performance Estimation**")

f_data = [
    ("W_total", W_total, "kg"),
    ("V_min", V_min, "m/sec"),
    ("V_drag", V_drag, "m/sec"),
    ("V_power", V_power, "m/sec"),
    ("V_margin", V_margin, "m/sec"),
    ("C_L", C_L, ""),
    ("C_D", C_D, ""),
    ("LD_ratio", L2DR , ""),
    ("time_of_flight", tof, "min"),
    ("range_of_flight", rof, "km")
]


#
df_f = pd.DataFrame(f_data, columns=["Parameter", "Value", "Unit"])

df_f["Value"] = df_f["Value"].map(lambda x: f"{x:.2f}")
#
halff = len(df_f) // 2 + len(df_f) % 2
df_leftf = df_f.iloc[:halff].reset_index(drop=True)
df_rightf = df_f.iloc[halff:].reset_index(drop=True)
#
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_leftf, hide_index=True, use_container_width=True)
with col2:
    st.dataframe(df_rightf, hide_index=True, use_container_width=True)