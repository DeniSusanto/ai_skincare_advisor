import * as React from "react";
import { View, Text } from "react-native";
import {
  createDrawerNavigator,
  DrawerContentScrollView,
  DrawerItemList,
} from "@react-navigation/drawer";
import Color from "../Cons/Color";
import Overall from "../Components/OverallReport";
import Acne from "../Components/AcneReport";
import Wrinkles from "../Components/WrinklesReport";
import CrowsFeet from "../Components/CrowsFeet";
import DarkEyeCircle from "../Components/DarkEyeCircleReport";

function CustomDrawerContent(props) {
  return (
    <DrawerContentScrollView {...props}>
      <DrawerItemList {...props} />
      {/* <DrawerItem
        label="Close drawer"
        onPress={() => props.navigation.closeDrawer()}
      />
      <DrawerItem
        label="Toggle drawer"
        onPress={() => props.navigation.toggleDrawer()}
      /> */}
    </DrawerContentScrollView>
  );
}

const Drawer = createDrawerNavigator();

function MyDrawer() {
  return (
    <Drawer.Navigator
      drawerContent={(props) => <CustomDrawerContent {...props} />}
      drawerStyle={{
        backgroundColor: Color.subtle_primary,
        width: "55%",
      }}
    >
      <Drawer.Screen name="Overall" component={Overall} />
      <Drawer.Screen name="Acne" component={Acne} />
      <Drawer.Screen name="Wrinkles" component={Wrinkles} />
      <Drawer.Screen name="Crow's Feet" component={CrowsFeet} />
      <Drawer.Screen name="Dark Eye Circle" component={DarkEyeCircle} />
    </Drawer.Navigator>
  );
}

export default function ReportScreen() {
  return <MyDrawer />;
}
