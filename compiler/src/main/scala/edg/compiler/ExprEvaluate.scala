package edg.compiler

import edg.expr.expr
import edg.lit.lit
import edg.ref.ref
import edg.wir.IndirectDesignPath

import scala.collection.Set


class ExprEvaluateException(msg: String) extends Exception(msg)

class ExprEvaluate(refs: ConstProp, root: IndirectDesignPath) extends ValueExprMap[ExprValue] {
  override def mapLiteral(literal: lit.ValueLit): ExprValue = literal.`type` match {
    case lit.ValueLit.Type.Floating(literal) => FloatValue(literal.`val`.toFloat)
    case lit.ValueLit.Type.Integer(literal) => IntValue(literal.`val`)
    case lit.ValueLit.Type.Boolean(literal) => BooleanValue(literal.`val`)
    case lit.ValueLit.Type.Text(literal) => TextValue(literal.`val`)
    case _ => throw new ExprEvaluateException(s"Unknown literal $literal")
  }

  override def mapBinary(binary: expr.BinaryExpr,
                         lhs: ExprValue, rhs: ExprValue): ExprValue = binary.op match {
      // Note promotion rules: range takes precedence, then float, then int
    case expr.BinaryExpr.Op.ADD => (lhs, rhs) match {
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        val all = Seq(lhsMin + rhsMin, lhsMin + rhsMax, lhsMax + rhsMin, lhsMax + rhsMax)
        RangeValue(all.min, all.max)
      case (RangeValue(lhsMin, lhsMax), FloatPromotable(rhs)) =>
        RangeValue(lhsMin + rhs, lhsMax + rhs)
      case (FloatPromotable(lhs), RangeValue(rhsMin, rhsMax)) =>
        RangeValue(lhs + rhsMin, lhs + rhsMax)
      case (FloatValue(lhs), FloatPromotable(rhs)) => FloatValue(lhs + rhs)
      case (FloatPromotable(lhs), FloatValue(rhs)) => FloatValue(lhs + rhs)
      case (IntValue(lhs), IntValue(rhs)) => IntValue(lhs + rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.SUB => (lhs, rhs) match {
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        val all = Seq(lhsMin - rhsMin, lhsMin - rhsMax, lhsMax - rhsMin, lhsMax - rhsMax)
        RangeValue(all.min, all.max)
      case (RangeValue(lhsMin, lhsMax), FloatPromotable(rhs)) =>
        RangeValue(lhsMin - rhs, lhsMax - rhs)
      case (FloatPromotable(lhs), RangeValue(rhsMin, rhsMax)) =>
        RangeValue(lhs - rhsMin, lhs - rhsMax)
      case (FloatValue(lhs), FloatPromotable(rhs)) => FloatValue(lhs - rhs)
      case (FloatPromotable(lhs), FloatValue(rhs)) => FloatValue(lhs - rhs)
      case (IntValue(lhs), IntValue(rhs)) => IntValue(lhs - rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.MULT => (lhs, rhs) match {
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        val all = Seq(lhsMin * rhsMin, lhsMin * rhsMax, lhsMax * rhsMin, lhsMax * rhsMax)
        RangeValue(all.min, all.max)
      case (RangeValue(lhsMin, lhsMax), FloatPromotable(rhs)) =>
        RangeValue(lhsMin * rhs, lhsMax * rhs)
      case (FloatPromotable(lhs), RangeValue(rhsMin, rhsMax)) =>
        RangeValue(lhs * rhsMin, lhs * rhsMax)
      case (FloatValue(lhs), FloatPromotable(rhs)) => FloatValue(lhs * rhs)
      case (FloatPromotable(lhs), FloatValue(rhs)) => FloatValue(lhs * rhs)
      case (IntValue(lhs), IntValue(rhs)) => IntValue(lhs * rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.DIV => (lhs, rhs) match {
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        val all = Seq(lhsMin / rhsMin, lhsMin / rhsMax, lhsMax / rhsMin, lhsMax / rhsMax)
        RangeValue(all.min, all.max)
      case (RangeValue(lhsMin, lhsMax), FloatPromotable(rhs)) =>
        RangeValue(lhsMin / rhs, lhsMax / rhs)
      case (FloatPromotable(lhs), RangeValue(rhsMin, rhsMax)) =>
        RangeValue(lhs / rhsMin, lhs / rhsMax)
      case (FloatValue(lhs), FloatPromotable(rhs)) => FloatValue(lhs / rhs)
      case (FloatPromotable(lhs), FloatValue(rhs)) => FloatValue(lhs / rhs)
      case (IntValue(lhs), IntValue(rhs)) => IntValue(lhs / rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.AND => (lhs, rhs) match {
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(lhs && rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.OR => (lhs, rhs) match {
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(lhs || rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.XOR => (lhs, rhs) match {
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(lhs ^ rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.IMPLIES => (lhs, rhs) match {
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(!lhs || rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.EQ => (lhs, rhs) match {
        // TODO can optionally support Range <-> Float ops later if desired, it's a 'type error' now
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        BooleanValue(lhsMin == rhsMin && lhsMax == rhsMax)
      case (IntValue(lhs), IntValue(rhs)) => BooleanValue(lhs == rhs)  // prioritize int compare before promotion
      case (FloatPromotable(lhs), FloatPromotable(rhs)) => BooleanValue(lhs == rhs)
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(lhs == rhs)
      case (TextValue(lhs), TextValue(rhs)) => BooleanValue(lhs == rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case expr.BinaryExpr.Op.NEQ => (lhs, rhs) match {
      // TODO can optionally support Range <-> Float ops later if desired, it's a 'type error' now
      case (RangeValue(lhsMin, lhsMax), RangeValue(rhsMin, rhsMax)) =>
        BooleanValue(lhsMin != rhsMin || lhsMax != rhsMax)
      case (IntValue(lhs), IntValue(rhs)) => BooleanValue(lhs != rhs)  // prioritize int compare before promotion
      case (FloatPromotable(lhs), FloatPromotable(rhs)) => BooleanValue(lhs != rhs)
      case (BooleanValue(lhs), BooleanValue(rhs)) => BooleanValue(lhs != rhs)
      case (TextValue(lhs), TextValue(rhs)) => BooleanValue(lhs != rhs)
      case _ => throw new ExprEvaluateException(s"Unknown binary operands in $lhs ${binary.op} $rhs from $binary")
    }

    case _ => throw new ExprEvaluateException(s"Unknown binary op in $lhs ${binary.op} $rhs from $binary")
  }


  override def mapReduce(reduce: expr.ReductionExpr, vals: ExprValue): ExprValue = vals

  override def mapStruct(struct: expr.StructExpr, vals: Map[String, ExprValue]): ExprValue =
    vals.values.flatten.toSet

  override def mapRange(range: expr.RangeExpr, minimum: ExprValue, maximum: ExprValue): ExprValue =
    minimum ++ maximum

  override def mapIfThenElse(ite: expr.IfThenElseExpr, cond: ExprValue,
                             tru: ExprValue, fal: ExprValue): ExprValue =
    cond ++ tru ++ fal

  override def mapExtract(extract: expr.ExtractExpr,
                          container: ExprValue, index: ExprValue): ExprValue =
    ???  // TODO need all elements of the container to be ready?

  override def mapMapExtract(mapExtract: expr.MapExtractExpr, container: ExprValue): ExprValue =
    ???  // TODO actually get all elements

  // connected and exported not overridden and to fail noisily
  // assign also not overridden and to fail noisily

  override def mapRef(path: ref.LocalPath): ExprValue = {
    Set(root ++ path)
  }

}
