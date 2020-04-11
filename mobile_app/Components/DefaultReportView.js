import * as React from "react";
import { View, ScrollView } from "react-native";
import { Button, Header, Icon } from "react-native-elements";
import Color from "../Cons/Color";
export default function DefaultReportView({ navigation, headbar, children }) {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "space-between",
        alignItems: "stretch",
      }}
    >
      <HeaderMenu navigation={navigation} headbar={headbar} />
      <ScrollView>{children}</ScrollView>
    </View>
  );
}

function HeaderMenu({ navigation, headbar }) {
  return (
    <Header
      statusBarProps={{ translucent: true }}
      leftComponent={
        <MenuIcon
          name="menu"
          navigate={() => navigation.toggleDrawer()}
          size={38}
        />
      }
      centerComponent={{
        text: headbar,
        style: { color: "#fff", fontSize: 22, fontWeight: "bold" },
      }}
      rightComponent={
        <MenuIcon
          name="local-mall"
          navigate={() => navigation.navigate("Products Recommendation")}
          size={32}
        />
      }
      backgroundColor={Color.primary}
    />
  );
}

function MenuIcon({ name, navigate, size }) {
  return (
    <Button
      icon={<Icon name={name} color="#fff" size={size} />}
      buttonStyle={{
        backgroundColor: "transparent",
      }}
      onPress={navigate}
    />
  );
}
