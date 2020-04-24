import * as React from "react";
import { View, ScrollView } from "react-native";
import { Input, Button, Icon, Header } from "react-native-elements";
import Color from "../Cons/Color";
import { Dropdown } from "react-native-material-dropdown";
import MultiSelect from "react-native-multiple-select";

export default function Questionnaire(props) {
  let [concerns, setConcerns] = React.useState([]);
  let [skinType, setSkinType] = React.useState("");
  let [preference, setPreference] = React.useState("");
  let [allergy, setAllergy] = React.useState("");
  let [age, setAge] = React.useState("");
  let [price, setPrice] = React.useState(null);
  function handleNavigation(
    navigation,
    age,
    skinType,
    concerns,
    preference,
    allergy,
    price
  ) {
    let props_data = {
      age: age,
      skin_type: skinType,
      concerns: concerns,
      preferences: preference,
      allergies: allergy,
      price: price,
    };
    // CHANGE THIS
    navigation.navigate("Take Image", props_data);
  }
  function handleMultiSelect(item) {
    setConcerns(item);
  }
  function processAge(value) {
    setAge(value);
  }
  function processSkinType(value) {
    value = value.toLowerCase();
    setSkinType(value);
  }

  let concern_data = [
    { id: "acne", value: "Acne" },
    { id: "dark_spots", value: "Dark Spots" },
    { id: "dryness", value: "Dryness" },
    { id: "dullness", value: "Dullness" },
    { id: "oiliness", value: "Oiliness" },
    { id: "pores", value: "Pores" },
    { id: "redness", value: "Redness" },
    { id: "uneven_skin_tone", value: "Uneven Skin Tone" },
    { id: "wrinkles", value: "Wrinkles" },
  ];

  let skin_type_data = [
    { value: "Combination" },
    { value: "Dry" },
    { value: "Normal" },
    { value: "Oily" },
  ];
  return (
    <View style={{ backgroundColor: "white", height: "100%" }}>
      <Header
        statusBarProps={{ translucent: true }}
        centerComponent={{
          text: "Questionnaire",
          style: { color: "#fff", fontSize: 22, fontWeight: "bold" },
        }}
        backgroundColor={Color.primary}
      />
      <ScrollView style={{ width: "100%" }}>
        <View
          style={{
            justifyContent: "flex-start",
            alignItems: "center",
            backgroundColor: "white",
            paddingVertical: 15,
          }}
        >
          <View
            style={{
              width: "90%",
              height: 600,
              justifyContent: "space-around",

              marginBottom: 15,
            }}
          >
            <Input
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="number-pad"
              maxLength={2}
              onChangeText={(age) => processAge(age)}
              value={age}
              placeholder="Age (Required)"
              placeholderTextColor="rgba(0, 0, 0, .38)"
              containerStyle={{
                width: "100%",
                paddingHorizontal: 0,
              }}
              labelStyle={{
                color: "black",
                fontSize: 16,
              }}
            />

            <Dropdown
              label="Skin Type (Required)"
              labelFontSize={18}
              data={skin_type_data}
              onChangeText={(value) => processSkinType(value)}
              labelTextStyle={{
                color: "black",
              }}
            />
            <MultiSelect
              items={concern_data}
              onSelectedItemsChange={(item) => handleMultiSelect(item)}
              selectedItems={concerns}
              uniqueKey="id"
              selectText="Pick Areas of Concerns"
              textColor="rgba(0, 0, 0, .38)"
              tagRemoveIconColor="red"
              tagBorderColor="green"
              tagTextColor="green"
              selectedItemTextColor="green"
              selectedItemIconColor="green"
              itemTextColor="#000"
              displayKey="value"
              searchInputStyle={{ color: "#CCC" }}
              submitButtonColor="green"
              submitButtonText="Confirm"
            />

            <Input
              autoCapitalize="none"
              autoCorrect={false}
              onChangeText={(value) => setPreference(value)}
              value={preference}
              placeholder="Skincare Product Preference (Optional)"
              placeholderTextColor="rgba(0, 0, 0, .38)"
              containerStyle={{
                width: "100%",
                paddingHorizontal: 0,
              }}
              labelStyle={{
                color: "black",
                fontSize: 16,
              }}
            />
            <Input
              autoCorrect={false}
              onChangeText={(value) => setAllergy(value)}
              value={allergy}
              placeholder="Ingridients Allergy (Optional)"
              placeholderTextColor="rgba(0, 0, 0, .38)"
              containerStyle={{
                width: "100%",
                paddingHorizontal: 0,
              }}
              labelStyle={{
                color: "black",
                fontSize: 16,
              }}
            />
            <Input
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="number-pad"
              onChangeText={(price) => setPrice(price)}
              value={price}
              placeholder="Maximum Price (Optional)"
              placeholderTextColor="rgba(0, 0, 0, .38)"
              labelStyle={{
                color: "black",
                fontSize: 16,
              }}
              leftIcon={
                <Icon
                  name="attach-money"
                  size={24}
                  color="black"
                  style={{ paddingHorizontal: 0 }}
                />
              }
              containerStyle={{
                width: "100%",
                paddingHorizontal: 0,
              }}
            />
          </View>
          <Button
            title="Proceed"
            buttonStyle={{
              backgroundColor: Color.darker_primary,
              paddingHorizontal: 40,
            }}
            containerStyle={{
              borderRadius: 20,
              overflow: "hidden",
            }}
            onPress={() =>
              handleNavigation(
                props.navigation,
                age,
                skinType,
                concerns,
                preference,
                allergy,
                price
              )
            }
          />
        </View>
      </ScrollView>
    </View>
  );
}
