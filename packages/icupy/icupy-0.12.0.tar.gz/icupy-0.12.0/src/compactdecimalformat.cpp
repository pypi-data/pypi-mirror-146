#include "main.hpp"
#include <pybind11/stl.h>

#if (U_ICU_VERSION_MAJOR_NUM >= 51)
#include <unicode/compactdecimalformat.h>
#endif // (U_ICU_VERSION_MAJOR_NUM >= 51)

using namespace icu;

void init_compactdecimalformat(py::module &m) {
#if (U_ICU_VERSION_MAJOR_NUM >= 51)
  // icu::CompactDecimalFormat
  py::class_<CompactDecimalFormat, DecimalFormat> cdf(m, "CompactDecimalFormat");
  cdf.def(py::init<const CompactDecimalFormat &>(), py::arg("source"));
  cdf.def("__copy__", &CompactDecimalFormat::clone)
      .def(
          "__deepcopy__", [](const CompactDecimalFormat &self, py::dict) { return self.clone(); }, py::arg("memo"));
  cdf.def("clone", &CompactDecimalFormat::clone);
  cdf.def_static(
      "create_instance",
      [](const _LocaleVariant &in_locale, UNumberCompactStyle style) {
        ErrorCode error_code;
        auto result = CompactDecimalFormat::createInstance(VARIANT_TO_LOCALE(in_locale), style, error_code);
        if (error_code.isFailure()) {
          throw ICUError(error_code);
        }
        return result;
      },
      py::arg("in_locale"), py::arg("style"));
  cdf.def(
         // [3] DecimalFormat::format
         "format", py::overload_cast<double, UnicodeString &, FieldPosition &>(&DecimalFormat::format, py::const_),
         py::arg("number").noconvert(), py::arg("append_to"), py::arg("pos"))
      .def(
          // [5] DecimalFormat::format
          "format",
          [](const DecimalFormat &self, double number, UnicodeString &append_to,
             FieldPositionIterator *pos_iter) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(number, append_to, pos_iter, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("number").noconvert(), py::arg("append_to"), py::arg("pos_iter"))
      // .def(
      //     // [6] DecimalFormat::format
      //     "format", py::overload_cast<int32_t, UnicodeString &, FieldPosition &>(&DecimalFormat::format, py::const_),
      //     py::arg("number"), py::arg("append_to"), py::arg("pos"))
      // .def(
      //     // [8] DecimalFormat::format
      //     "format",
      //     [](const DecimalFormat &self, int32_t number, UnicodeString &append_to,
      //        FieldPositionIterator *pos_iter) -> UnicodeString & {
      //       ErrorCode error_code;
      //       auto &result = self.format(number, append_to, pos_iter, error_code);
      //       if (error_code.isFailure()) {
      //         throw ICUError(error_code);
      //       }
      //       return result;
      //     },
      //     py::arg("number").noconvert(), py::arg("append_to"), py::arg("pos_iter"))
      .def(
          // [9] DecimalFormat::format
          "format", py::overload_cast<int64_t, UnicodeString &, FieldPosition &>(&DecimalFormat::format, py::const_),
          py::arg("number"), py::arg("append_to"), py::arg("pos"))
      .def(
          // [11] DecimalFormat::format
          "format",
          [](const DecimalFormat &self, int64_t number, UnicodeString &append_to,
             FieldPositionIterator *pos_iter) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(number, append_to, pos_iter, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("number").noconvert(), py::arg("append_to"), py::arg("pos_iter"))
      .def(
          // [12] DecimalFormat::format
          "format",
          [](const DecimalFormat &self, const char *number, UnicodeString &append_to,
             FieldPositionIterator *pos_iter) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(StringPiece(number), append_to, pos_iter, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("number").noconvert(), py::arg("append_to"), py::arg("pos_iter"))
      .def(
          "format",
          [](const NumberFormat &self, const Formattable &obj, UnicodeString &append_to,
             FieldPosition &pos) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(obj, append_to, pos, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("obj"), py::arg("append_to"), py::arg("pos"))
      .def(
          "format",
          [](const NumberFormat &self, const Formattable &obj, UnicodeString &append_to,
             FieldPositionIterator *pos_iter) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(obj, append_to, pos_iter, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("obj"), py::arg("append_to"), py::arg("pos_iter"))
      .def("format", py::overload_cast<double, UnicodeString &>(&NumberFormat::format, py::const_),
           py::arg("number").noconvert(), py::arg("append_to"))
      // .def("format", py::overload_cast<int32_t, UnicodeString &>(&NumberFormat::format, py::const_),
      //      py::arg("number"), py::arg("append_to"))
      .def("format", py::overload_cast<int64_t, UnicodeString &>(&NumberFormat::format, py::const_), py::arg("number"),
           py::arg("append_to"))
      .def(
          "format",
          [](const Format &self, const Formattable &obj, UnicodeString &append_to) -> UnicodeString & {
            ErrorCode error_code;
            auto &result = self.format(obj, append_to, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
            return result;
          },
          py::arg("obj"), py::arg("append_to"));
  cdf.def(
         // [1] CompactDecimalFormat::parse
         "parse",
         [](const CompactDecimalFormat &self, const _UnicodeStringVariant &text, Formattable &result,
            ParsePosition &parse_position) { self.parse(VARIANT_TO_UNISTR(text), result, parse_position); },
         py::arg("text"), py::arg("result"), py::arg("parse_position"))
      .def(
          // [2] CompactDecimalFormat::parse
          "parse",
          [](const CompactDecimalFormat &self, const _UnicodeStringVariant &text, Formattable &result) {
            ErrorCode error_code;
            self.parse(VARIANT_TO_UNISTR(text), result, error_code);
            if (error_code.isFailure()) {
              throw ICUError(error_code);
            }
          },
          py::arg("text"), py::arg("result"));
#endif // (U_ICU_VERSION_MAJOR_NUM >= 51)
}
